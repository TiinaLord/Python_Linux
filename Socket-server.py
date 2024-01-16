import socket
import http


def get_status_code(status_code):
    try:
        return http.HTTPStatus(status_code).phrase
    except ValueError:
        return "500 Internal Server Error"


def handle_connection(client_socket):
    request = client_socket.recv(1024)
    request_lines = request.decode().split("\n")

    method, path, _ = request_lines[0].split(" ")
    status_code = get_status_code(int(path.split("=")[1]))

    response = """HTTP/1.1 {status_code} {status_phrase}

    Request Method: {method}
    Request Source: {source}
    Response Status: {status_code}

    {headers}
    """.format(
        status_code=status_code,
        status_phrase=http.HTTPStatus(status_code).phrase,
        method=method,
        source=client_socket.getpeername(),
        headers="\n".join(
            f"{header_name}: {header_value}" for header_name, header_value in request_lines[1:]
        ),
    )

    client_socket.sendall(response.encode())
    client_socket.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(("localhost", 80))
    server_socket.listen(1)

    while True:
        client_socket, _ = server_socket.accept()
        handle_connection(client_socket)
