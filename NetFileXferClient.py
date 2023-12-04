import socket
import ssl
import sys
import os

'''
This program is a client that sends files to a server.
It implements TLS integration and ssl context to wrap the connected socket.

@see
    The ssl context for client side is referenced from this site.
    https://asecuritysite.com/subjects/chapter107

@author
    Jemina Maasin, mostly implemented this code to have SSL implementation
    Prof. Ibrahim El-Shekeil, helped me out on minor bugs
    
'''

def send_file(server_ip, server_port, file_path):
    """Send a file to the server.
    
    Args:
        server_ip (str): IP address of the server.
        server_port (int): Port number of the server.
        file_path (str): Path of the file to be sent.
    """

    # Ensure that the given file exists
    assert os.path.exists(file_path), "File not found."
    
    # Create a client socket using IPv4 and TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # IMPLEMENTATION OF SSL IN CLIENT-SIDE
    # Sets up the SSL context for client side
    context = ssl.create_default_context()  # feedback from prof to keep this
    context.check_hostname = False  # if removed, it will cause prompt errors in the terminal
    context.verify_mode = ssl.CERT_NONE  # if removed, it will cause certificate verification failure

    # Sets up the SSL context wraps on all client_socket using TLS
    secure_client_connection = context.wrap_socket(client_socket, server_hostname=server_ip)

    try:
        secure_client_connection.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        # Extract file name from path
        file_name = file_path.split('/')[-1]
        
        # Send the length of the file name to the server
        secure_client_connection.send(len(file_name.encode()).to_bytes(4, byteorder='big'))
        
        # Send the actual file name
        secure_client_connection.send(file_name.encode())
        
        # Open and send file
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                secure_client_connection.send(data)

        print("File sent successfully.")

    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        secure_client_connection.close()
        print(f"Connection to {server_ip}:{server_port} closed.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: client.py <SERVER_IP> <SERVER_PORT> <FILE_PATH>")
        sys.exit(1)

    server_ip = sys.argv[1]
    
    try:
        server_port = int(sys.argv[2])
        assert 1024 <= server_port <= 65535, "Port number should be between 1024 and 65535."

        file_path = sys.argv[3]
        send_file(server_ip, server_port, file_path)
    except ValueError:
        print("Port should be a number.")
