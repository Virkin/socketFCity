import synchro_pb2
import socket
import mysql.connector
import sys

import testProto
import time
import struct

def recv_message(connection,sz):
        data = list()
        transferred_bytes= 0
        while transferred_bytes < sz:
            data.append(connection.recv(min(sz-transferred_bytes, 2048)))
            if not data[-1]:
                raise RuntimeError("socket connection broken")
            transferred_bytes += len(data[-1])
        return b''.join(data)

class ClientSocket :

    def __init__(self):
        self.HOST = "172.17.3.241"
        self.PORT = 8080

        self.protobufProcess = testProto.ProtobufProcessing("Car", "localhost", "root", "root", "fcity")

        self.protobufProcess.clearDb()

        data = synchro_pb2.CarToServ()
        data.connectionRequest.Clear()
        # Create a socket (SOCK_STREAM means a TCP socket)
        self.fSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            # Connect to server and send data
            self.fSock.connect((self.HOST, self.PORT))
            self.fSock.sendall(data.SerializeToString())

            # Receive data from the server and shut down
            recv = self.fSock.recv(1024)
         
            msg = synchro_pb2.ServToCar.FromString(recv)
        except Exception as e:
            raise(e)

        print("Sent:     {}".format(data.SerializeToString()))
        print("Received: {}".format(msg.connectionResponse.port))

        self.PORT = msg.connectionResponse.port
        
        
        # Create a socket (SOCK_STREAM means a TCP socket)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE,1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

        self.progress = 0

    def startRide(self) :
        try:
            data = synchro_pb2.CarToServ()
            data.synchronizeRequest.Clear()
            # Connect to server and send data
            data = data.SerializeToString()

            self.sock.connect((self.HOST, self.PORT))
            s=struct.pack(">L",len(data))+data
            self.sock.send(s)

            # Receive data from the server and shut down
            print("J'attend les données du serveur qui fou rien")

            bf = self.sock.recv(4)
            sz=struct.unpack(">L",bf)[0]
            recv = recv_message(self.sock, sz)

            # Receive all element of the server database
            self.protobufProcess.protobufElementToDb(recv)

            msg = protobufProcess.startRide()
            s=struct.pack(">L",len(msg))+msg
            self.sock.send(s)

            recv = self.sock.recv(1024)

            if self.protobufProcess.isTaskDone(recv) != True :
                print("The server socket doesnt return response for the start ride")
                sys.exit(1)

        except Exception as e:
            raise(e)

    def getCurrentRide(self) :
        if self.protobufProcess.setCurrentRide() == -1 :
            print("No ride has been booked")
            return -1
        else :
            return self.protobufProcess.setCurrentRide()

    def getProgress(self):
        return self.progress

    def endRide(self):
        try:    

            msg = self.protobufProcess.generateDataMsg().SerializeToString()

            self.progress += 1

            s=struct.pack(">L",len(msg))+msg
            self.sock.send(s)

            self.progress += 1

            recv = self.sock.recv(1024)

            self.progress += 1

            if self.protobufProcess.isTaskDone(recv) == True :
                self.sock.close()
                self.progress +=1

        except Exception as e:
            raise(e)

        print("Sent:     {}".format(data))
        print("Received: {}".format(recv))

        data = synchro_pb2.CarToServ()
        data.endConnectionRequest.Clear()

        try :
            self.fSock.send(data.SerializeToString())
        except Exception as e:
            raise(e)
        finally :
            self.fSock.close()

