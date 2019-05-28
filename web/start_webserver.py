import SocketServer
import requestHandler

port = 8000

def definitely_not_printing(s):
	print(s)

Handler = requestHandler.CustomHandler
Handler.add_post_listener(definitely_not_printing)
httpd = SocketServer.TCPServer(("", port), Handler)
print('serving on port {0}'.format(port))
httpd.serve_forever()
