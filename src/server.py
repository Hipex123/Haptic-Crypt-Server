import socket, re

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = ("localhost", XXXX)
tcpSocket.bind(address)

tcpSocket.listen(1)

while True:
    print("Waiting for connection...")
    connection, client = tcpSocket.accept()

    try:
        print("Client connected")
         
        while True:
            data = connection.recv(1024)
            formatedData = str(data)[2:-3]

            f1 = re.sub(r"\\\\", r"\\", formatedData)
            f2 = re.sub(r"\\\\", r"\\", f1)

            if len(f2) != 0:
                print(f2)
 
            if not data:
                break
    finally:
        connection.close()