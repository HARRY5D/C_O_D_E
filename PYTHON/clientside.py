# import socket
# import threading

# # Function to receive messages from the server
# def receive_messages(client_socket):
#     while True:
#         try:
#             message = client_socket.recv(1024).decode('utf-8')
#             if message:
#                 print(f'Server: {message}')
#         except:
#             client_socket.close()
#             break

# # Set up the client
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('127.0.0.1', 8000))

# # Start a thread to receive messages
# threading.Thread(target=receive_messages, args=(client_socket,)).start()

# # Send messages to the server
# while True:
#     message = input('You: ')
#     client_socket.send(message.encode('utf-8'))


# import socket

# def start_client():
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         client.connect(('127.0.0.1', 5555))
#         print("[CONNECTED] Connected to server!")
        
#         while True:
#             message = input("> ")
#             if message.lower() == 'quit':
#                 break
            
#             client.send(message.encode())
#             response = client.recv(1024).decode()
#             print(f"Server: {response}")
            
#     except ConnectionRefusedError:
#         print("[ERROR] Server is not running!")
#     finally:
#         client.close()

# if __name__ == "__main__":
#     start_client()

import socket
import sys

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(('127.0.0.1', 5555))
        print("[CONNECTED] Connected to server!")
        
        while True:
            try:
                message = input("> ")
                if message.lower() == 'quit':
                    print("[CLOSING] Connection closed by user")
                    break
                
                client.send(message.encode('utf-8'))
                response = client.recv(1024).decode('utf-8')
                print(f"Server: {response}")
                
            except ConnectionResetError:
                print("[ERROR] Server connection was lost")
                break
            except KeyboardInterrupt:
                print("\n[CLOSING] Connection closed by user")
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                break
                
    except ConnectionRefusedError:
        print("[ERROR] Could not connect to server. Is it running?")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client.close()

if __name__ == "__main__":
    try:
        start_client()
    except KeyboardInterrupt:
        sys.exit(0)