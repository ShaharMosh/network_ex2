import socket
import sys
import os


## Read file as bytes and return the data.
def printImg(fileName): 
    data = ''
    path = 'files/files' + fileName
    file = open(path, 'rb')
    data = file.read()
    file.close()
    return data

## Check the suffix of the file, read the data and return it.
def printFile(fileName):
    data = ''
    path = 'files/files' + fileName
    endFile = fileName.split('.')[1] ## Get the suffix of the file.

    ## Check the suffix of the file and read accordingly.
    if endFile == 'ico' or endFile == 'jpg':
        data = printImg(fileName)

    else:
        file = open(path, encoding = "ISO-8859-1")
        line = file.readline()
        while line:
            if (len(line.split('<u>')) > 1):
                data += (str)(line.split('<u>')[1]).split('</u>')[0]

            line = file.readline()
        data = data.encode("utf-8")
        file.close()
        
    return data

## Get the name of the file.
def getFileName(data):
    fileName = data.split(' ')[1]
    ## Check if the name file is '/'- we want the index.html file.
    if fileName == '/':
        fileName = "/index.html"
    return fileName

## Create the message to send to the client.
def messageToClient(data):
    status = data.split()[2] 
    fileName = getFileName(data)
    
    ## Check if the file is in the directory.
    if(fileExist(fileName)):
        ## Message we send if the file name is 'redirect'.
        if fileName == 'redirect':
            status += " 301 Moved Permanetly"
            connection = "Connection: close"
            location = "Location: /result.html"
            message = status + '\n' + connection + '\n' + location + '\n\n'
        else:
            ## If the file name is the directory
            status += " 200 OK"
            connection = data.split('\n')[2].split('\r')[0]
            contentFile = printFile(fileName)
            length = "Content-Length: " + (str)(len(contentFile))
            message = status + '\n' + connection + '\n' + length  + '\n\n'
    else:
        ## If the file is not in the directory.
        status += " 404 Not Found"
        connection = "Connection: close"
        message = status + '\n' + connection + '\n\n'

    return message
        

# Check if file exist in the directory.
def fileExist(fileName):
    path = 'files/files' + fileName
    return os.path.exists(path)
    


## Get data from the command line and check if valid.
args = sys.argv
#if(len(args) == 2 and args[1].isnumeric() and (int)(args[1]) in range(0, 65535)):
#  port = (int)(args[1])

## Create socket.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 8081))
server.listen(5)

while True:
        client_socket, client_address = server.accept()
        #print('Connection from: ', client_address)
        print('here')
        data = client_socket.recv(100)
        print('Received:', data)
        dataStr = data.decode("utf-8")
        ## Create the massage(the content and its details) and send to the client.
        message = str.encode(messageToClient(dataStr))
        content = printFile(getFileName(dataStr))
        client_socket.send(message + content)
        
        ## Check if the client ask to close the conncection.
        connection = dataStr.split('\n')[2].split('\r')[0]
        if connection == "Connection: close":
            client_socket.close()
