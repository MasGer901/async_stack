import socket
import selectors


class Subject:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()
    selector = selectors.DefaultSelector()


class SendMessage(Subject):

    def send_message(self, client_socket):
        request = client_socket.recv(4096)

        if request:
            response = "Hello world\n".encode()
            client_socket.send(response)
        else:
            print("Outside inner while loop")
            self.selector.unregister(client_socket)
            client_socket.close()


class AcceptConnection(SendMessage):

    def accept_connection(self, server_socket):
        client_socket, addr = server_socket.accept()
        print("Connect from", addr)
        self.selector.register(fileobj=client_socket, events=selectors.EVENT_READ,
                               data=self.send_message)


class Controller(AcceptConnection, SendMessage):

    def event_loop(self):
        self.accept_connection(server_socket=self.server_socket)
        self.selector.register(fileobj=self.server_socket, events=selectors.EVENT_READ, data=self.accept_connection)

        while True:
            events = self.selector.select()
            for key, _ in events:
                callback = key.data
                callback(key.fileobj)


if __name__ == '__main__':
    control = Controller()
    control.event_loop()
