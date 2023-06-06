import socket
from select import select


class Subject:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()

    to_read = {}
    to_write = {}
    tasks = []


def server():
    while True:

        yield 'read', Subject.server_socket
        client_socket, addr = Subject.server_socket.accept()

        print("Connect from", addr)
        Subject.tasks.append(client(client_socket))


def client(client_socket):
    while True:

        yield 'read', client_socket
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            response = "Hello world\n".encode()

            yield "write", client_socket
            client_socket.send(response)

    print("Outside inner while loop")
    client_socket.close()


def event_loop():
    Subject.tasks.append(server())

    while any([Subject.tasks, Subject.to_read, Subject.to_write]):

        while not Subject.tasks:
            ready_to_read, ready_to_write, _ = select(Subject.to_read, Subject.to_write, [])

            for sock in ready_to_read:
                Subject.tasks.append(Subject.to_read.pop(sock))

            for sock in ready_to_write:
                Subject.tasks.append(Subject.to_write.pop(sock))

        try:
            task = Subject.tasks.pop(0)

            reason, sock = next(task)
            if reason == "read":
                Subject.to_read[sock] = task
            if reason == "write":
                Subject.to_write[sock] = task

        except StopIteration:
            pass


if __name__ == '__main__':
    event_loop()
