import socket

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
            data = connection.recv(32)
            formattedData = str(data)[2:-1]
            newData = list(formattedData)

            for i in range(len(formattedData)):
                if formattedData[i] == "\\":
                    newData[i], newData[i + 1] = "", ""

            formattedData = "".join(newData)
            if len(formattedData) != 0:
                print(formattedData)
 
            if not data:
                break
    finally:
        connection.close()