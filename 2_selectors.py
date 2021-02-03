import socket
import selectors
import sys

selector = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    selector.register(
        fileobj=server_socket,
        events=selectors.EVENT_READ,
        data=accept_connection
    )


def accept_connection(server_socket_fun):
    print('The server is waiting for connection')
    client_socket, addr = server_socket_fun.accept()
    print('Connection from', addr)
    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_message
    )


def send_message(client_socket):
    print('Server is waiting until client will write something')
    request = client_socket.recv(4096)

    if request:
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        print('The client was killed')
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:
        try:
            events = selector.select()
        except KeyboardInterrupt:
            sys.exit()

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
