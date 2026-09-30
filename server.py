from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs
import crud_clientes
import logica_impuesto
import json

port = 3000
crudClientes = crud_clientes.crud_clientes()
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

        if ruta == "/cliente":
            respuesta = {'msg': crudClientes.administrar(datos)}
            self._responder_json(respuesta)
            return

        if ruta == "/periodo_impuesto":
            respuesta = logicaImp.guardar_periodo(datos)
            self._responder_json(respuesta)
            return

        if ruta == "/calcular_impuesto":
            balance = float(datos.get('balance', 0))
            producto = int(datos.get('producto_codigo', 11801))
            respuesta = logicaImp.calcular(balance, producto)
            self._responder_json(respuesta)
            return

        self._responder_json({'msg': 'Ruta no encontrada'}, 404)

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)

        if urlParse.path == "/clientes":
            buscar = qs.get('buscar', [''])[0]
            datos = crudClientes.consultar(buscar)   # ← AQUÍ ESTABA EL BUG
            self._responder_json(datos if datos is not None else [])
            return

        if urlParse.path == "/periodos_impuesto":
            cliente_id = qs.get('cliente_id', [''])[0]
            datos = logicaImp.consultar_periodos(cliente_id)
            self._responder_json(datos if datos is not None else [])
            return

        if self.path == "/":
            self.path = "/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        return SimpleHTTPRequestHandler.do_GET(self)


print(f"Servidor corriendo en el puerto {port}")
server = HTTPServer(("localhost", port), miServidor)
server.serve_forever()