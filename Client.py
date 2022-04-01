#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import time


IP = socket.gethostbyname(socket.gethostname())
PORT = 6789  
ADDR = (IP, PORT)
SIZE= 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(ADDR)

while True:
    inp = input('')
    if inp.split()[0] == 'download' and inp.split()[1] == 'all':
        server.send(bytes(inp, 'utf-8'))
        length = int(server.recv(SIZE).decode('utf-8'))
        a=[]
        for i in range(length):
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((socket.gethostname(), 6789))
            file_name = client.recv(SIZE).decode('utf-8')
            a.append(file_name)
            file_size = client.recv(SIZE).decode('utf-8')
            with open(file_name, "wb") as file:
                size = 0
                while size <= int(file_size):
                    data = client.recv(SIZE)
                    if not data:
                        break
                    file.write(data)
                    size += len(data)
                client.close()
        print('Downloaded ',end='')
        for i in a:
            print(i,end=' ')
        print()




    elif inp.split()[0] == 'download':
        server.send(bytes(inp, 'utf-8'))
        file_name = inp.split()[1]
        
        file_size = server.recv(SIZE).decode('utf-8')
       
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)           
        client.bind((socket.gethostname(), 9876))
   
        with open(file_name, "wb") as file:
            size = 0
            while size <= int(file_size):                
                conn = client.recv(SIZE)             
                file.write(conn)                
                size += len(conn)                
                if size == int(file_size):                    
                    client.close()
                    break
        print('Downloaded', file_name)
        
    elif inp == 'exit':        
        print('Exitting...')
        time.sleep(0.05)        
        server.close()
        print('Server Closed Successfully')
        exit(0)
    

    else:
        server.send(bytes(inp, 'utf-8'))
        msg = server.recv(SIZE)
        print(msg.decode('utf-8'))
        
    


# In[ ]:




