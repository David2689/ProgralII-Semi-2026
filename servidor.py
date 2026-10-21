import http.server
import socketserver
import json
import mysql.connector
from urllib.parse import urlparse, parse_qs

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '', 
    'database': 'db_academica'
}

def crud_usuarios_usss001825(accion, datos=None):
    """
    Método principal para el CRUD.
    accion: 'crear', 'buscar', 'actualizar', 'eliminar', 'login'
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True) 
        
        respuesta = {"status": "error", "mensaje": "Acción no válida"}

        if accion == 'crear':
            sql = "INSERT INTO usuarios_usss001825 (usuario, clave, nombre, direccion, telefono) VALUES (%s, %s, %s, %s, %s)"
            valores = (datos['usuario'], datos['clave'], datos['nombre'], datos['direccion'], datos['telefono'])
            cursor.execute(sql, valores)
            conn.commit()
            respuesta = {"status": "ok", "mensaje": "Usuario registrado exitosamente"}

        elif accion == 'buscar':
            termino = f"%{datos['termino']}%"
            sql = "SELECT * FROM usuarios_usss001825 WHERE usuario LIKE %s OR nombre LIKE %s"
            cursor.execute(sql, (termino, termino))
            resultados = cursor.fetchall()
            respuesta = {"status": "ok", "data": resultados}

        elif accion == 'actualizar':
            sql = "UPDATE usuarios_usss001825 SET usuario=%s, clave=%s, nombre=%s, direccion=%s, telefono=%s WHERE idUsuario=%s"
            valores = (datos['usuario'], datos['clave'], datos['nombre'], datos['direccion'], datos['telefono'], datos['idUsuario'])
            cursor.execute(sql, valores)
            conn.commit()
            respuesta = {"status": "ok", "mensaje": "Usuario actualizado"}

        elif accion == 'eliminar':
            sql = "DELETE FROM usuarios_usss001825 WHERE idUsuario=%s"
            cursor.execute(sql, (datos['idUsuario'],))
            conn.commit()
            respuesta = {"status": "ok", "mensaje": "Usuario eliminado"}

        elif accion == 'login':

            sql = "SELECT * FROM usuarios_usss001825 WHERE usuario=%s AND clave=%s"
            cursor.execute(sql, (datos['usuario'], datos['clave']))
            user = cursor.fetchone()
            if user:
                respuesta = {"status": "ok", "mensaje": "Acceso concedido", "usuario": user}
            else:
                respuesta = {"status": "error", "mensaje": "Credenciales incorrectas"}

        return respuesta

    except mysql.connector.Error as err:
        return {"status": "error", "mensaje": f"Error de BD: {err}"}
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

class MiServidor(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/' or self.path == '/login.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('login.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/usuarios.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('usuarios.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        datos = json.loads(post_data.decode('utf-8'))
        
        accion = ''
        if self.path == '/api/crear': accion = 'crear'
        elif self.path == '/api/buscar': accion = 'buscar'
        elif self.path == '/api/actualizar': accion = 'actualizar'
        elif self.path == '/api/eliminar': accion = 'eliminar'
        elif self.path == '/api/login': accion = 'login'

        resultado = crud_usuarios_usss001825(accion, datos)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(resultado).encode('utf-8'))

if __name__ == '__main__':
    PORT = 8000
    with socketserver.TCPServer(("", PORT), MiServidor) as httpd:
        print(f"Servidor corriendo en http://localhost:{PORT}")
        print("Abre tu navegador en http://localhost:8000 para ver el Login")
        httpd.serve_forever()