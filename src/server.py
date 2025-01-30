import socket, re, threading

userCount = 0

users = {}

def removeUser(username):
    global users, userCount

    if username in users:
        del users[username]
        userCount -= 1

def userCheck(username):
    global users

    if username in users:
        raise KeyError

    return username

def sendMsg(clientSocket, msg):
    try:
        clientSocket.sendall(msg.encode("utf-8"))
    except:
        return None

def handleClient(connection, client):
    global users, userCount

    username = ""

    try:
        print("Client connected")

        while True:
            data = connection.recv(8192)

            if str(data)[2:18] == "CONNECTED|PH0NE|":
                users[userCheck(str(data)[18:-1])] = connection
                username = str(data)[18:-1]
                userCount += 1

                print(users)
                continue
            
            if str(data)[2:-1] == "CL0SE|CONNECTION|PHONE":
                removeUser(username)
                print("USER REMOVED")
                break
            
            formatedData = str(data)[2:-3]
            
            f1 = re.sub(r'\s*\d+$', '', formatedData)
            f2 = re.sub(r"\\\\", r"\\", f1)
            f3 = re.sub(r"\\\\", r"\\", f2)

            sendMsg(users[username], f3)

            if not data:
                break

    except KeyError:
        sendMsg(connection, "Username taken")
    except:
        print("EXC")
        connection.close()
    finally:
        print("FNL")
        print(users)
        connection.close()

def startServer(ip, port):
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcpSocket.bind((ip, port))

    tcpSocket.listen(5)    
        
    while True:
        connection, client = tcpSocket.accept()
        threading.Thread(target=handleClient, args=(connection, client), daemon=True).start()

startServer("XXXX", XXXX)