import SimpleHTTPServer
import SocketServer

PORT = 8888

handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), handler)

httpd.serve_forever()
