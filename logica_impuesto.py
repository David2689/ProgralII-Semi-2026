import math

class LogicaImpuesto:
    def __init__(self, conexion_db):
        self.db = conexion_db

    def buscar_tarifa(self, balance, producto_codigo):
        sql = """
            SELECT id, desde, hasta, precio_base, adicional, porcentaje
            FROM tarifas_actividades
            WHERE producto_codigo = %s
              AND %s >= desde
              AND %s <= hasta
        """
        tarifas = self.db.consultar(sql, (producto_codigo, balance, balance))
        if tarifas is None:
            return None, "Error al consultar la tabla tarifaria."
        if len(tarifas) > 1:
            return None, "Existe más de una tarifa aplicable. Corrija la tabla tarifaria."
        if len(tarifas) == 0:
            return None, "No existe una tarifa configurada para el balance indicado."
        return tarifas[0], None

    def calcular(self, balance, producto_codigo):
        if balance is None or float(balance) <= 0:
            return {"error": "Ingrese un balance mayor que cero."}
        balance = float(balance)
        tarifa, error = self.buscar_tarifa(balance, producto_codigo)
        if error:
            return {"error": error}
        desde = float(tarifa['desde'])
        precio_base = float(tarifa['precio_base'])
        adicional = float(tarifa['adicional'])
        porcentaje = float(tarifa['porcentaje'])
        if porcentaje > 0:
            impuesto = balance * (porcentaje / 100.0)
            formula = f"Balance ({balance}) x {porcentaje}% = {impuesto:.2f}"
            bloques = 0
            excedente = 0
        else:
            excedente = balance - desde
            if excedente <= 0:
                bloques = 0
            else:
                bloques = math.ceil(excedente / 1000.0)
            impuesto = precio_base + (bloques * adicional)
            formula = f"Base {precio_base} + ({bloques} x {adicional}) = {impuesto:.2f}"
        return {
            "exito": True,
            "balance": balance,
            "producto_codigo": producto_codigo,
            "rango_desde": desde,
            "rango_hasta": float(tarifa['hasta']),
            "precio_base": precio_base,
            "adicional": adicional,
            "porcentaje": porcentaje,
            "excedente": round(excedente, 2),
            "bloques": bloques,
            "precio_calculado": round(impuesto, 6),
            "precio_mostrar": round(impuesto, 2),
            "formula_usada": formula
        }

    def guardar_periodo(self, datos):
        try:
            cliente_id = datos.get('cliente_id')
            producto_codigo = datos.get('producto_codigo')
            fecha_desde = datos.get('fecha_desde')
            fecha_hasta = datos.get('fecha_hasta')
            balance = float(datos.get('balance', 0))
            if not cliente_id:
                return {"msg": "Debe seleccionar un cliente."}
            if not fecha_desde or not fecha_hasta:
                return {"msg": "Debe ingresar las fechas Desde y Hasta."}
            if fecha_desde >= fecha_hasta:
                return {"msg": "La fecha Hasta debe ser posterior a la fecha Desde."}
            if balance <= 0:
                return {"msg": "Ingrese un balance mayor que cero."}
            sql_verif = """
                SELECT id FROM periodos_impuestos
                WHERE cliente_id = %s
                  AND producto_codigo = %s
                  AND (fecha_desde < %s AND fecha_hasta > %s)
            """
            superpuestos = self.db.consultar(sql_verif, (cliente_id, producto_codigo, fecha_hasta, fecha_desde))
            if superpuestos is None:
                return {"msg": "Error al verificar superposición."}
            if len(superpuestos) > 0:
                return {"msg": "El período indicado se superpone con un período existente."}
            resultado = self.calcular(balance, producto_codigo)
            if "error" in resultado:
                return {"msg": resultado["error"]}
            sql_insert = """
                INSERT INTO periodos_impuestos
                (cliente_id, producto_codigo, fecha_desde, fecha_hasta, balance,
                 precio_calculado, formula_usada, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Vigente')
            """
            valores = (
                cliente_id, producto_codigo, fecha_desde, fecha_hasta, balance,
                resultado['precio_calculado'], resultado['formula_usada']
            )
            res = self.db.ejecutar(sql_insert, valores)
            if res != 'ok':
                return {"msg": f"Error al guardar: {res}"}
            return {"msg": "ok", "detalle": resultado}
        except Exception as e:
            return {"msg": f"Error inesperado: {e}"}

    def consultar_periodos(self, cliente_id):
        sql = """
            SELECT id, cliente_id, producto_codigo, fecha_desde, fecha_hasta,
                   balance, precio_calculado, formula_usada, estado
            FROM periodos_impuestos
            WHERE cliente_id = %s
            ORDER BY fecha_desde ASC
        """
        return self.db.consultar(sql, (cliente_id,))