import synchro_pb2
import socket
import socketserver
import mysql.connector

import testProto

import threading
import struct

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

	protobufProccess = testProto.ProtobufProcessing("Serv", "localhost", "root", "root", "fcity")

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
				sz=struct.unpack(">L",bf)[0]
				print("\n{} bytes\n".format(sz))
				self.data = self.recv_message(self.request,sz)

				msg = synchro_pb2.CarToServ.FromString(self.data);

				if msg.HasField("synchronizeRequest") :
					
					resp = self.protobufProccess.generateProto()
					s=struct.pack(">L",len(resp))+resp
					self.request.sendall(s)

				elif msg.HasField("endOfRideRequest") :
					print("end of ride !!!!")
					self.protobufProccess.protobufDataToDb(msg)

					resp = self.protobufProccess.generateDataResp()
					self.request.sendall(resp)
					shutdown = True

			except Exception as e :
				raise(e)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class MyTCPHandler(socketserver.StreamRequestHandler):

	def handle(self):
		# self.rfile is a file-like object created by the handler;
		# we can now use e.g. readline() instead of raw recv() calls

		data = self.request.recv(1024)

		msg = synchro_pb2.CarToServ.FromString(data);

		print("Msg : '{}'".format(data));

		if msg.HasField("connectionRequest") :
			print(" Connection Request !!!")
			
			for port in carPort :
				try :
					threadedSocket = ThreadedTCPServer((HOST, port), ThreadedTCPRequestHandler)

					server_thread = threading.Thread(target=threadedSocket.serve_forever)
					server_thread.daemon = True
					server_thread.start()

					resp = synchro_pb2.ServToCar()
					resp.connectionResponse.port = port
					self.wfile.write(resp.SerializeToString())

					data = self.request.recv(1024)
					msg = synchro_pb2.CarToServ.FromString(data);

					if msg.HasField("endConnectionRequest") :
						print("\nshutdown socket")
						threadedSocket.server_close()
						threadedSocket.shutdown()

					break;
				except Exception as e :
					print(e)


if __name__ == "__main__":
	
	HOST, PORT = "localhost", 8080
	carPort = list(range(8090, 8100))
	server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()
	
