import socket
import ssl

'''
This program is a server that reads client's files.
It implements TLS integration and ssl context to wrap the connected socket.

@see
    The ssl context for server side is referenced from this site.
    https://asecuritysite.com/subjects/chapter107
    
@author
    Jemina Maasin, mostly modified this code
'''

def start_server(port):
    """Start the file transfer server.
    
    Args:
        port (int): Port on which the server should listen.
    """
    # Assert port is a valid value
    assert 1024 <= port <= 65535, "Port number should be between 1024 and 65535."

    # Create the server socket using IPv4 and TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server address and port
    server_socket.bind(('localhost', port))
    server_socket.listen(5)  # Listen with a backlog of 5 connections

    # Sets up the SSL context and uses the cert.pem and key.pem inside the server directory
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # if 'ssl.Purpose.CLIENT_AUTH' removed, it will cause connection reset. The client won't be connected.
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    print(f"Server listening on port {port}...")

    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Wraps the accepted client socket by securing it using TLS
        secure_client_connection = context.wrap_socket(client_socket, server_side=True)

        # First, receive the 4-byte file name length. The socket connection is also wrapped
        file_name_length = int.from_bytes(secure_client_connection.recv(4), byteorder='big')

        try:
            # Now, receive the actual file name
            file_name = secure_client_connection.recv(file_name_length).decode()
            print(f"Receiving file named: {file_name}\n" + "*" * 80)

            # Receive the file content and save it
            with open(file_name, 'wb') as file:
                while True:
                    data = secure_client_connection.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    
            print(f"Received file {file_name}")

        except Exception as e:
            print(f"Error: {e}")

        secure_client_connection.close()
        print(f"Connection with {client_address} closed.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: server.py <PORT>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        start_server(port)
    except ValueError:
        print("Port should be a number.")

