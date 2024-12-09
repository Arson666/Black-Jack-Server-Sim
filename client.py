import socket

def run_client(server_address, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))

    while True:
        server_message = client_socket.recv(1024).decode()
        print(server_message)

        if "Goodbye!" in server_message:
            break

        user_input = input()
        client_socket.send(user_input.encode())

    client_socket.close()

if __name__ == "__main__":
    # Specify the server address and port number
    server_address = "localhost"
    server_port = 12345

    run_client(server_address, server_port)