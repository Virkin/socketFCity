import synchro_pb2
import socket
import socketserver
import mysql.connector

import testProto

import threading
import struct
import time
"""socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 8080))

while True:
        socket.listen(5)
        client, address = socket.accept()
        print("{} connected".format( address ))

        response = client.recv(255)
        if response != "":
                user = fcityData_pb2.User.FromString(response)
                print("name : {}".format(user.name))

print("Close")
client.close()
stock.close()"""

class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):

	protobufProccess = testProto.ProtobufProcessing("Serv", "localhost", "fcity", "fcity29217!", "fcity2")

	def recv_message(self, connection,sz):
	    data = list()
	    transferred_bytes= 0
	    while transferred_bytes < sz:
	        data.append(connection.recv(min(sz-transferred_bytes, 2048)))
	        if not data[-1]:
	            raise RuntimeError("socket connection broken")
	        transferred_bytes += len(data[-1])
	    return b''.join(data)

	def handle(self):
		shutdown = False
		while not shutdown :
			try :
		
				bf = self.request.recv(4)
				
				if bf != b'' :
					sz=struct.unpack(">L",bf)[0]
				
					print("\n{} bytes\n".format(sz))
					self.data = self.recv_message(self.request,sz)

					msg = synchro_pb2.CarToServ.FromString(self.data);

					if msg.HasField("synchronizeRequest") :
						resp = self.protobufProccess.generateProto()
						s=struct.pack(">L",len(resp))+resp
						self.request.sendall(s)

					elif msg.HasField("startOfRideRequest") :
						resp = self.protobufProccess.setStartRide(msg)
						self.request.sendall(resp)

					elif msg.HasField("endOfRideRequest") :
						print("end of ride !!!!")
						self.protobufProccess.protobufDataToDb(msg)

						resp = self.protobufProccess.generateDataResp()
						self.request.sendall(resp)
						shutdown = True
				else :
					time.sleep(1)

			except Exception as e :
				raise(e)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class MyTCPHandler(socketserver.StreamRequestHandler):

	threadedSocket = {}

	def handle(self):

		data = self.request.recv(1024)

		msg = synchro_pb2.CarToServ.FromString(data);

		print("Msg : '{}'".format(data));

		if msg.HasField("connectionRequest") :
			print(" Connection Request !!!")
			
			for port in carPort :
				try :
					self.threadedSocket[port] = ThreadedTCPServer((HOST, port), ThreadedTCPRequestHandler)

					server_thread = threading.Thread(target=self.threadedSocket[port].serve_forever)
					server_thread.daemon = True
					server_thread.start()

					resp = synchro_pb2.ServToCar()
					resp.connectionResponse.port = port
					self.wfile.write(resp.SerializeToString())

					break;
		
				except Exception as e :
					print(e)

		elif msg.HasField("endConnectionRequest") :
			print("\nshutdown socket")
			port = msg.endConnectionRequest.port
			self.threadedSocket[port].server_close()
			self.threadedSocket[port].shutdown()





if __name__ == "__main__":
	
	HOST, PORT = "172.31.3.59", 8080
	carPort = list(range(8090, 8190))
	server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()
	
