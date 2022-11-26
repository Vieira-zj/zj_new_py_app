# coding=utf-8

from http.server import HTTPServer, BaseHTTPRequestHandler

IP = '127.0.0.1'
PORT = 8081


class Handler(BaseHTTPRequestHandler):
    '''
    curl http://127.0.0.1:8081
    '''

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = 'py http server'
        self.wfile.write(bytes(message, 'utf8'))


def run():
    with HTTPServer((IP, PORT), Handler) as httpd:
        print('py http serving at port:', PORT)
        httpd.serve_forever()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt as e:
        print('cancelled, and http server exit')
    except Exception as e:
        print('system exception:', e)
