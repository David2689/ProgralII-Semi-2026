from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse 
from urllib.parse import urlparse, parse_qs
import crud_clientes
import crud_productos
import logica_impuesto
import json

port = 3000
crudClientes = crud_clientes.crud_clientes()
crudProductos = crud_productos.crud_productos()
logicaImp = logica_impuesto.LogicaImpuesto(crud_clientes.db)


class miServidor(SimpleHTTPRequestHandler):

    def _responder_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode("utf-8"))

    def do_POST(self):
        longitud = int(self.headers['Content-Length'])
        datos = self.rfile.read(longitud)
        datos = datos.decode("utf-8")
        datos = parse.unquote(datos)
        datos = json.loads(datos)

        ruta = urlparse(self.path).path

        # Ruta unificada por campo "modulo" (del ingeniero)
        if ruta == "/":
            modulo = datos.get("modulo", "")
            if modulo == "cliente":
                self._responder_json({'msg': crudClientes.administrar(datos)})
                return
            elif modulo == "producto":
                self._responder_json({'msg': crudProductos.administrar(datos)})
                return
            elif modulo == "periodo_impuesto":
                self._responder_json(logicaImp.guardar_periodo(datos))
                return
            elif modulo == "calcular_impuesto":
                balance = float(datos.get('balance', 0))
                producto = int(datos.get('producto_codigo', 11801))
                self._responder_json(logicaImp.calcular(balance, producto))
                return

        # Rutas directas (para compatibilidad con productos.html del ingeniero)
        if ruta == "/cliente":
            self._responder_json({'msg': crudClientes.administrar(datos)})
            return
        if ruta == "/producto":
            self._responder_json({'msg': crudProductos.administrar(datos)})
            return
        if ruta == "/periodo_impuesto":
            self._responder_json(logicaImp.guardar_periodo(datos))
            return
        if ruta == "/calcular_impuesto":
            balance = float(datos.get('balance', 0))
            producto = int(datos.get('producto_codigo', 11801))
            self._responder_json(logicaImp.calcular(balance, producto))
            return

        self._responder_json({'msg': 'Ruta no encontrada'}, 404)

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)

        if urlParse.path == "/clientes":
            buscar = qs.get('buscar', [''])[0]
            self._responder_json(crudClientes.consultar(buscar) or [])
            return

        if urlParse.path == "/productos":
            buscar = qs.get('buscar', [''])[0]
            self._responder_json(crudProductos.consultar(buscar) or [])
            return

        if urlParse.path == "/periodos_impuesto":
            cliente_id = qs.get('cliente_id', ['0'])[0]
            self._responder_json(logicaImp.consultar_periodos(cliente_id) or [])
            return

        if urlParse.path == "/vistas":
            form = qs.get('form', [''])[0]
            self.path = f"/modulos/{form}.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        if self.path == "/":
            self.path = "/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        return SimpleHTTPRequestHandler.do_GET(self)


print(f"Servidor corriendo en el puerto {port}")
server = HTTPServer(("localhost", port), miServidor)
server.serve_forever()