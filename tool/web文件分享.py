import http.server
import socketserver,os

PORT = 8000
DIRECTORY = r'D:\\'

handler = http.server.SimpleHTTPRequestHandler
os.chdir(DIRECTORY)
handler.directory = DIRECTORY

with socketserver.TCPServer(("", PORT), handler) as file:
    print("serving at port", PORT)
    file.serve_forever()