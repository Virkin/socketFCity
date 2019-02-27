import synchro_pb2
import fcityDatabase_pb2
import mysql.connector
import datetime
import random
import time

class ProtobufProcessing() :
	def __init__(self, mode, host, user, passwd, database) :
		
		self.mode = mode

		self.mydb = mysql.connector.connect(
  			host=host,
  			user=user,
 			passwd=passwd,
  			database=database
		)

	def addElement(self, element, table, row) :
		curs = self.mydb.cursor(dictionary=True)

		curs.execute("SHOW columns FROM {}".format(table))

		result = curs.fetchall()

		for column in result :
			setattr(element, column["Field"], str(row[column["Field"]]))

		curs.close()
		
	def generateProto(self) :
		resp = synchro_pb2.ServToCar()
		resp.synchronizeResponse.Clear()

		curs = self.mydb.cursor(dictionary=True)

		for table in synchro_pb2.table.keys() :
			if table == "data" :
				continue
			else :
				curs.execute("SELECT * FROM {}".format(table))

				result = curs.fetchall()

				for row in result :
					self.addElement(getattr(resp.synchronizeResponse.element, table).add(), table, row)

		print("Msg : {}".format(resp))

		curs.close()

		return resp.SerializeToString()

	def insertElement(self, element, table) :
		curs = self.mydb.cursor(dictionary=True)

		curs.execute("SHOW columns FROM {}".format(table))

		resultCol = curs.fetchall()

		for row in getattr(element,table) :
			request = "INSERT INTO {} VALUES(".format(table)

			for column in resultCol :
					if getattr(row,column["Field"]) == "None" :
						request += "NULL,"
					else :
						request += "'{}',".format(getattr(row,column["Field"]))

			request = request[:-1] + ");"

			print("Req : {}\n".format(request))

			curs.execute(request)

		curs.close()

	def insertData(self, element):
		print("elem : {}".format(element))
		table = "data"
		print("INSERT data !!!!")
		curs = self.mydb.cursor(dictionary=True)

		curs.execute("SHOW columns FROM {}".format(table))

		resultCol = curs.fetchall()

		count = 0

		for row in getattr(element,table) :
			request = "INSERT INTO {} VALUES(".format(table)

			for column in resultCol :
					if getattr(row,column["Field"]) == "None" or column["Field"] == "id":
						request += "NULL,"
					else :
						request += "'{}',".format(getattr(row,column["Field"]))

			request = request[:-1] + ");"

			count += 1
			print("\n{}\n".format(count))

			print("Req : {}\n".format(request))

			curs.execute(request)

		curs.close()
	
	def protobufElementToDb(self, msg) :
		curs = self.mydb.cursor(dictionary=True)

		msg = synchro_pb2.ServToCar.FromString(msg);

		print("Msg : {}".format(msg))

		for table in synchro_pb2.table.keys() :
			self.insertElement(msg.synchronizeResponse.element, table)

		curs.close()
		
		self.mydb.commit()

	def protobufDataToDb(self,msg) :
		curs = self.mydb.cursor(dictionary=True)

		self.insertData(msg.endOfRideRequest.element)

		curs.close()
		
		self.mydb.commit()

	def clearDb(self) :
		curs = self.mydb.cursor(dictionary=True)
		
		curs.execute("SET FOREIGN_KEY_CHECKS=0;")
		
		for table in synchro_pb2.table.keys() :
			curs.execute("TRUNCATE TABLE {}".format(table))

		curs.execute("SET FOREIGN_KEY_CHECKS=1;")

		curs.close()
		
		self.mydb.commit()

	def insertFakeData(self) :
		curs = self.mydb.cursor()

		curs.execute("SELECT count(*) FROM users")
		result = curs.fetchone()

		nbUser = result[0] 
		
		now = datetime.datetime.now()

		for i in range(nbUser) :
			voltage = 240
			for j in range(100) : 
				speed = round(random.uniform(20,30),2)
				curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(i+2,1,speed,now.strftime('%Y-%m-%d %H:%M:%S')))
				curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(i+2,1,voltage,now.strftime('%Y-%m-%d %H:%M:%S')))
				now += datetime.timedelta(0,1)

				if i==0 :
					voltage -= 0.05
				else :
					voltage -= 0.02
		
		curs.close()
		self.mydb.commit()

	def generateDataMsg(self) :
		msg = synchro_pb2.CarToServ()
		msg.endOfRideRequest.Clear()

		table = "data"

		curs = self.mydb.cursor(dictionary=True)

		curs.execute("SELECT * FROM {}".format(table))

		result = curs.fetchall()

		for row in result :
			self.addElement(getattr(msg.endOfRideRequest.element, table).add(), table, row)

		curs.close()

		return msg

	def generateData(self) :
		self.insertFakeData()
		msg = self.generateDataMsg()

		print(msg)

		return msg.SerializeToString()

	def generateDataResp(self) :
		msg = synchro_pb2.ServToCar()
		msg.endOfRideResponse.taskDone = True
		return msg.SerializeToString()

	def isTaskDone(self, msg) :
		msg = synchro_pb2.ServToCar()

		if msg.HasField("endOfRideResponse") :
			if msg.endOfRideResponse.taskDone == True :
				return True
			else :
				return False
		else :
			return False





if __name__ == "__main__":
	
	processServ = ProtobufProcessing("Serv", "localhost", "root", "root", "fcity")
	processCar = ProtobufProcessing("Car", "localhost", "root", "root", "fcity_client")

	msg = processServ.generateProto()

	processCar.protobufDataToDb(msg)
	