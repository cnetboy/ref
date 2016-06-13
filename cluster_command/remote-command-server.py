import pyjsonrpc
import subprocess

class RequestHandler(pyjsonrpc.HttpRequestHandler):

  @pyjsonrpc.rpcmethod
  def do_command(self, command):

    output = subprocess.check_output(command, shell=True)
    '''subprocess.call(command, shell=True)'''
    return output


# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('', 8080),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://localhost:8080"
http_server.serve_forever()
