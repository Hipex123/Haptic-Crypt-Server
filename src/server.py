import socket, threading

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
                #sendMsg(users["usr0"], "   x0196,   m109,  xdd,   x0162,   x01b6,   m64,   x019b, e,  xd9,  1, 97, 3uamsfhe6b"+"|"+"33731209164B66D5A685B71172027F725ACD41E125705CE180157C6A71F828FD")
                continue
            
            elif str(data)[2:-1] == "CL0SE|CONNECTION|PHONE":
                removeUser(username)
                print("USER REMOVED")
                break
            
            formatedData = str(data)[2:-1]

            msg = formatedData[:formatedData.find("|")-2]

            receiver = formatedData[formatedData.find("|")+1:formatedData.rfind("|")]

            identifier = formatedData[formatedData.rfind("|")+1:]

            try:
                print(msg)
                sendMsg(users[receiver], " "+msg+"|"+identifier)
            except:
                continue

            if not data:
                break

    except KeyError:
        sendMsg(connection, "Username taken")
    except:
        print("EXC")
        connection.close()
    finally:
        try:
            if (username in users):
                removeUser(username)
                print("USER REMOVED")
        except:
            pass
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

startServer("localhost", 30000)
