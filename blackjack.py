import threading
import server
import client

# Run the server and client in separate threads
def run_game():
    server_thread = threading.Thread(target=server.start_server, args=(12345,))
    client_thread = threading.Thread(target=client.run_client, args=("localhost", 12345))

    server_thread.start()
    client_thread.start()

    server_thread.join()
    client_thread.join()

if __name__ == "__main__":
    run_game()