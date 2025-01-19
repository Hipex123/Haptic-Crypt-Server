import socket, re

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = ("XXXX", XXXX)
tcpSocket.bind(address)

tcpSocket.listen(1)

userCount = 0

users = {

}

while True:
    print("Waiting for connection...")
    connection, client = tcpSocket.accept()

    try:
        print("Client connected")
        while True:
            data = connection.recv(8192)
            if str(data)[2:-1] == "CONNECTED|PH0NE":
                userCount += 1
                users[userCount] = client[0]
                continue

            formatedData = str(data)[2:-3]

            f1 = re.sub(r"\\\\", r"\\", formatedData)
            f2 = re.sub(r"\\\\", r"\\", f1)

            if len(f2) != 0:
                print(f2)

            if not data:
                break
    except:
        connection.close()
    finally:
        connection.close()