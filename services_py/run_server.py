from services_py.api import create_server

if __name__ == '__main__':
    server = create_server(8080)
    print('GenUI API listening on http://0.0.0.0:8080')
    server.serve_forever()
