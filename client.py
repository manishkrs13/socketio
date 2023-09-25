import socket 
import sys 
import os

s = socket.socket() 
HOST = '127.0.0.1'
PORT = 7002
s.connect((HOST, PORT))

msg = input('Enter message to send to server. DOWNLOAD or UPLOAD : ')
s.send(msg.encode('ascii')) 
if msg == 'KILL':
    sys.exit()
elif msg == 'DOWNLOAD': 
    print('Files on the server : ')
    files = s.recv(1024).decode('ascii') 
    print(files)
    file_name = input('Enter the file name to download : ') 
    s.send(file_name.encode())
    with open(file_name, 'wb') as f: 
        data = s.recv(1024)
    while data:
        f.write(data)
        data = s.recv(1024) 
        print('File Downloaded!') 
        s.close()
elif msg == 'UPLOAD':
    print('Files on the client : ') 
    file_names = ""
    with os.scandir('./') as files: 
        for file in files:
            file_names = file_names + str(file.name) + '\n'
    print(file_names)
    file_name = input('Enter the file name to upload : ') 
    s.send(file_name.encode('ascii'))
    try:
        with open(file_name, 'rb') as f: 
            data = f.read() 
            s.sendall(data)
    except FileNotFoundError: 
        print('File Not Found')
    print('File Uploaded!') 
    s.close()
