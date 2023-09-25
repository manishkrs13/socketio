import os 
import socket

s = socket.socket()
PORT = 7002
s.bind(('localhost', PORT)) 
print('Server is running') 
print('Welcome to Your Server') 
s.listen(5)
flag = True 
while flag:
    connection, address = s.accept()
    msg = connection.recv(1024).decode('ascii') 
    print(msg)
    if msg == 'KILL': 
        flag = False
        connection.close() 
    elif msg == 'DOWNLOAD':
        file_name = ""
        with os.scandir('./') as files: 
            for file in files:
                file_name = file_name + str(file.name) +'\n'
            connection.send(file_name.encode('ascii')) 
        file_name = connection.recv(1024).decode('ascii') 
        print(file_name)
        try:
            with open(file_name, 'rb') as f: 
                data = f.read() 
                connection.sendall(data)
        except FileNotFoundError:
            print('File Not Found')
        connection.close() 
    elif msg == 'UPLOAD':
        file_name = connection.recv(1024).decode('ascii') 
        with open(file_name, 'wb') as f:
            data = connection.recv(1024)
            while data:
                f.write(data)
                data = connection.recv(1024) 
            connection.send('Received'.encode('ascii'))
        connection.close() 
connection.close()

