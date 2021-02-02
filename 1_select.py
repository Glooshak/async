import socket
from select import select


to_monitor = list()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()


def accept_connection(server_socket_fun):
    print('The server is waiting for connection')
    client_socket, addr = server_socket_fun.accept()
    print('Connection from', addr)
    to_monitor.append(client_socket)


def send_message(client_socket):
    print('Server is waiting until client will write something')
    request = client_socket.recv(4096)

    if request:
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        print('The client was killed')
        client_socket.close()
        to_monitor.remove(client_socket)


def event_loop():
    while True:
        try:
            ready_to_read, _, _ = select(to_monitor, [], [])
        except KeyboardInterrupt:
            exit()

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()
