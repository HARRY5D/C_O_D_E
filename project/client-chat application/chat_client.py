
#--------------------------------------------------------------------------------

## 2. chat_client.py

# filepath: chat_client.py
import socket
import ssl
import threading

# Server configuration (must match the server)
HOST = '127.0.0.1'
PORT = 5555
CA_CERT_FILE = 'server.crt'  # The trusted CA/server certificate

def receive_messages(tls_client_socket):
    """
    Continuously listens for messages from the server and displays them.
    """
    while True:
        try:
            message = tls_client_socket.recv(1024)
            if not message:
                break
            print(message.decode('utf-8'))
        except:
            break

def start_client():
    """
    Connect to the chat server over TLS and allow sending/receiving messages.
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile=CA_CERT_FILE)
    context.verify_mode = ssl.CERT_REQUIRED
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Secure (wrap) the client socket
        with context.wrap_socket(client_socket, server_hostname=HOST) as tls_client_socket:
            tls_client_socket.connect((HOST, PORT))
            print(f"[CONNECTED] Connected securely to {HOST}:{PORT}")
            
            # Start a thread to listen for incoming messages
            thread = threading.Thread(target=receive_messages, args=(tls_client_socket,))
            thread.start()

            while True:
                message = input("")
                if message.lower() == 'quit':
                    break
                try:
                    tls_client_socket.send(message.encode('utf-8'))
                except:
                    print("[ERROR] Failed to send message.")
                    break

if __name__ == "__main__":
    start_client()