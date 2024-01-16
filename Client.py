import socket


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 80))

    request = "GET /?status=200 HTTP/1.1\n\n"
    client_socket.sendall(request.encode())

    response = client_socket.recv(1024)
    print(response.decode())


if __name__ == "__main__":
    main()
