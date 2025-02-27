
# filepath: chat_server.py
import socket
import ssl
import threading

# Server configuration
HOST = '127.0.0.1'  # Listen on localhost
PORT = 5555        # Port to listen on
CERT_FILE = 'server.crt'  # Path to server certificate
KEY_FILE = 'server.key'   # Path to server private key

clients = []

def broadcast_message(message, sender_socket=None):
    """
    Send a message to all connected clients except the sender.
    """
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                pass

def handle_client(client_socket, client_address):
    print(f"[CONNECTED] {client_address} connected.")
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            broadcast_message(data, client_socket)
        except:
            break

    # Client disconnected
    print(f"[DISCONNECTED] {client_address} disconnected.")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    """
    Create an SSL context, wrap the socket, and handle incoming client connections.
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"[STARTING] Secure chat server is listening on {HOST}:{PORT}...")

        # Wrap socket with SSL
        with context.wrap_socket(server_socket, server_side=True) as tls_server_socket:
            while True:
                # Wait for client connections
                client_conn, client_addr = tls_server_socket.accept()
                clients.append(client_conn)
                
                # Start a thread to handle communication with the new client
                thread = threading.Thread(target=handle_client, args=(client_conn, client_addr))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()