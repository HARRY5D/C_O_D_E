# import socket
# import threading

# # Function to handle client connections
# def handle_client(client_socket):
#     while True:
#         try:
#             message = client_socket.recv(1024).decode('utf-8')
#             if message:
#                 print(f'Received: {message}')
#                 broadcast_message(message, client_socket)
#         except:
#             clients.remove(client_socket)
#             client_socket.close()
#             break

# # Function to broadcast messages to all clients
# def broadcast_message(message, sender_socket):
#     for client in clients:
#         if client != sender_socket:
#             client.send(message.encode('utf-8'))

# # Set up the server
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(('0.0.0.0', 8000))
# server_socket.listen(5)
# print('Server listening on port 8000')

# clients = []

# # Accept client connections
# while True:
#     client_socket, client_address = server_socket.accept()
#     print(f'Accepted connection from {client_address}')
#     clients.append(client_socket)
#     threading.Thread(target=handle_client, args=(client_socket,)).start()


# import socket
# import threading

# def handle_client(client_socket, address):
#     print(f"[NEW CONNECTION] {address} connected.")
    
#     while True:
#         try:
#             message = client_socket.recv(1024).decode()
#             if not message:
#                 break
#             print(f"[{address}] {message}")
#             client_socket.send("Message received!".encode())
#         except:
#             break
    
#     print(f"[DISCONNECTED] {address}")
#     client_socket.close()

# def start_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(('127.0.0.1', 5555))
#     server.listen()
#     print("[STARTING] Server is listening...")
    
#     while True:
#         client, address = server.accept()
#         thread = threading.Thread(target=handle_client, args=(client, address))
#         thread.start()
#         print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# if __name__ == "__main__":
#     start_server()


import socket
import threading
import sys

def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"[DISCONNECTED] {address}")
                break
            print(f"[{address}] {message}")
            client_socket.send("Message received!".encode('utf-8'))
        except ConnectionResetError:
            print(f"[ERROR] Connection reset by {address}")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            break
    
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('127.0.0.1', 5555))
        server.listen(5)
        print("[STARTING] Server is listening on port 5555...")
        
        while True:
            try:
                client, address = server.accept()
                thread = threading.Thread(target=handle_client, args=(client, address))
                thread.daemon = True  # Allow Ctrl+C to stop server
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            except KeyboardInterrupt:
                print("\n[STOPPING] Server is shutting down...")
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                break
                
    except OSError as e:
        print(f"[ERROR] {e}")
    finally:
        server.close()

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        sys.exit(0)