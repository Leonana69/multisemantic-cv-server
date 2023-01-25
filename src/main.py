import http.server
from http_server import MultisemanticHTTPServerHandler

if __name__ == "__main__":
    HOST, PORT = '192.168.1.144', 50001
    with http.server.HTTPServer((HOST, PORT), MultisemanticHTTPServerHandler) as server:
        print("Server start...")
        server.serve_forever()
