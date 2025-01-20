import socket, re, threading

userCount = 0

users = {}

def removeUser(cli):
    global users, userCount

    for key, val in users.items():
        if val == cli:
            del users[key]
            userCount -= 1
            break

def findFreeSpot():
    global users, userCount

    prevKey = 0
    for key in users.keys():
        if key - prevKey != 1:
            return key - 1
        prevKey = key
    return userCount

def sendMsg(clientSocket, msg):
    try:
        clientSocket.sendall(msg.encode("utf-8"))
    except:
        return None

def handleClient(connection, client):
    global users, userCount

    try:
        print("Client connected")
        print(f"U-{userCount}")
        print(f"D-{len(users)}")
        while True:
            data = connection.recv(8192)

            if str(data)[2:-1] == "CONNECTED|PH0NE":
                userCount += 1
                users[findFreeSpot()] = connection
                continue
            
            if str(data)[2:-1] == "CL0SE|CONNECTION|PHONE":
                removeUser(connection)
                break
            
            formatedData = str(data)[2:-3]
            
            # preF = re.findall(r"\d+", formatedData)

            # f0 = preF[-1] if preF else None
            f1 = re.sub(r'\s*\d+$', '', formatedData)
            f2 = re.sub(r"\\\\", r"\\", f1)
            f3 = re.sub(r"\\\\", r"\\", f2)

            sendMsg(users[1], f3)

            if not data:
                break
    except:
        connection.close()
    finally:
        connection.close()

def startServer(ip, port):
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcpSocket.bind((ip, port))

    tcpSocket.listen(5)    
        
    while True:
        connection, client = tcpSocket.accept()
        threading.Thread(target=handleClient, args=(connection, client), daemon=True).start()

startServer("XXXX", XXXX)