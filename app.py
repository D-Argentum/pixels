from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import numpy as np
import tensorflow as tf
#
# # Cargar el modelo entrenado
model = tf.keras.models.load_model('/Users/fortknox/PycharmProjects/pixels/trained_model.h5')
#
# class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
#     def do_POST(self):
#         if self.path == '/':
#             self.handle_prediction_request()
#         else:
#             self.send_error(404, "Not Found")
#
#     def handle_prediction_request(self):
#         content_length = int(self.headers['Content-Length'])
#         data = self.rfile.read(content_length)
#         data = data.decode().replace('pixels=', '')
#         data = parse.unquote(data)
#
#         # Realizar transformación para dejar igual que los ejemplos que usa MNIST
#         arr = np.fromstring(data, dtype=np.float32, sep=',')
#         arr = arr.reshape(28, 28)
#         arr = np.array(arr)
#         arr = arr.reshape(1, 28, 28, 1)
#
#         # Realizar y obtener la predicción
#         prediction_values = model.predict(arr, batch_size=1)
#         prediction = str(np.argmax(prediction_values))
#         print("Predicción final:", prediction)
#
#         # Regresar respuesta a la petición HTTP
#         self.send_response(200)
#         self.send_header("Content-type", "text/plain")
#         self.end_headers()
#         self.wfile.write(prediction.encode())
#
#     def do_GET(self):
#         if self.path == '/':
#             self.send_response(200)
#             self.send_header("Content-type", "text/html")
#             self.end_headers()
#             self.wfile.write(b"<html><body><h1>Hello, world!</h1></body></html>")
#         elif self.path == '/favicon.ico':
#             self.send_response(404)
#             self.end_headers()
#         else:
#             self.send_error(404, "Not Found")
#
# if __name__ == '__main__':
#     print("Iniciando el servidor...")
#     server_address = ('localhost', 8000)
#     httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
#     print('Servidor en ejecución en http://localhost:8000/')
#     httpd.serve_forever()


from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # Ruta completa al archivo index.html
            index_path = '/Users/fortknox/PycharmProjects/pixels/templates/index.html'

            # Verificar si el archivo existe
            if os.path.exists(index_path):
                with open(index_path, 'rb') as file:
                    html_content = file.read()
                self.wfile.write(html_content)
            else:
                self.wfile.write("Error: Archivo no encontrado".encode())
        elif self.path == '/favicon.ico':
            self.send_response(404)
            self.end_headers()
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode().replace('pixels=', '')
        data = parse.unquote(data)

        # Realizar transformación para dejar igual que los ejemplos que usa MNIST
        arr = np.fromstring(data, dtype=np.float32, sep=',')
        arr = arr.reshape(28, 28)
        arr = np.array(arr)
        arr = arr.reshape(1, 28, 28, 1)

        # Realizar y obtener la predicción
        prediction_values = model.predict(arr, batch_size=1)
        prediction = str(np.argmax(prediction_values))
        print("Predicción final:", prediction)


        # Regresar respuesta a la peticion HTTP
        self.send_response(200)
        # Evitar problemas con CORS
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(prediction.encode())

if __name__ == '__main__':
    print("Iniciando el servidor...")
    server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    print('Servidor en ejecución en http://localhost:8000/')
    server.serve_forever()
