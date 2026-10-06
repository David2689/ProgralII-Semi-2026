import mysql.connector
from mysql.connector import Error


class Conexion:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "db_sistema_impuestos"
        print("Conectando a la base de datos...")

        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conexion.is_connected():
                print("Conexion exitosa")
            else:
                print("No se pudo conectar a la base de datos")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def _verificar_conexion(self):
        try:
            if not self.conexion.is_connected():
                print("Reconectando a la base de datos...")
                self.conexion.reconnect(attempts=3, delay=1)
        except Error as e:
            print(f"Error al reconectar: {e}")
            try:
                self.conexion = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            except Error as e2:
                print(f"Reconexion fallida: {e2}")

    def consultar(self, sql, datos=None):
        self._verificar_conexion()
        try:
            cursor = self.conexion.cursor(dictionary=True)
            if datos:
                cursor.execute(sql, datos)
            else:
                cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Error al consultar: {e}")
            return None

    def ejecutar(self, sql, datos=None):
        self._verificar_conexion()
        try:
            cursor = self.conexion.cursor()
            if datos:
                cursor.execute(sql, datos)
            else:
                cursor.execute(sql)
            self.conexion.commit()
            return 'ok'
        except Error as e:
            print(f"Error al ejecutar: {e}")
            return f'Error: {e}'