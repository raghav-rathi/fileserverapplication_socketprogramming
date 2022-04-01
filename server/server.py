#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import os
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 6789 
ADDR = (IP, PORT)
SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print('Server Started...')

while True:
    conn, addr = server.accept()
    while conn:
        try:
            msg = conn.recv(SIZE).decode('utf-8')
            if msg == 'listallfiles':
                message=''
                fileread = os.listdir(os.curdir)
                if len(fileread) == 0:
                    message += ("The server directory is empty")
                else:
                    for i in fileread:
                        message += str(i) + ' '
                    conn.send(bytes(message, 'utf-8'))

            elif msg.split()[0] == 'download' and msg.split()[1] == 'all':
                fileread = os.listdir(os.curdir)
                length = len(fileread)
                conn.send(str(length).encode('utf-8'))
                for i in fileread:
                    conn2, addr2 = server.accept()
                    file_name = i
                    conn2.send(file_name.encode('utf-8'))
                    time.sleep(0.05) 
                    file_size = os.path.getsize(file_name)
                    conn2.send(str(file_size).encode('utf-8'))
                    with open(file_name, "rb") as file:
                        size = 0
                        while size <= file_size:
                            data = file.read(SIZE)
                            if not (data):
                                break
                            conn2.sendall(data)
                            size += len(data)
                        conn2.close()
            elif msg.split()[0] == 'download':
                file_name = msg.split()[1]                
                file_size = os.path.getsize(file_name)                
                conn.send(str(file_size).encode('utf-8'))
                server1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                
                with open(file_name, "rb") as file:
                    size = 0
                    while size <= file_size:
                        data = file.read(SIZE)
                        if not data:
                            break
                        server1.sendto(data, (socket.gethostname(), 9876))
                        time.sleep(0.05)                        
                        size += len(data)     
                    
                    server1.close()

            
               
        except :
            conn = False


# In[ ]:




