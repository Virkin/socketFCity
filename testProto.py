import synchro_pb2
import fcityDatabase_pb2
import mysql.connector
import datetime
import random
import time
import math
import lzma 

class ProtobufProcessing() :
	def __init__(self, mode, host, user, passwd, database) :
		
		self.mode = mode
		self.currentRideId = 1

		self.host=host
		self.user=user
		self.passwd=passwd
		self.database=database

		self.mydb = mysql.connector.connect(
  			host=self.host,
  			user=self.user,
 			passwd=self.passwd,
  			database=self.database
		)

	def resetDbConnection(self):
		self.mydb = mysql.connector.connect(
  			host=self.host,
  			user=self.user,
 			passwd=self.passwd,
  			database=self.database
		)

		
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
			print(msg.synchronizeResponse.element)
			self.insertElement(msg.synchronizeResponse.element, table)

		curs.close()
		
		self.mydb.commit()

	def protobufDataToDb(self,msg) :
		curs = self.mydb.cursor(dictionary=True)

		data = msg.endOfRideRequest.data
		data = str(lzma.decompress(data))

		curs.execute("UPDATE ride SET end_date='{}' WHERE id='{}'".format(msg.endOfRideRequest.endDate, msg.endOfRideRequest.id))

		while data.find("{") != -1 :
			startPos = data.find("{")
			endPos = data.find("}")
			row = data[startPos+1:endPos]
			data = data[endPos+1:]
			elm = row.split(',')
			#print("mId : {} / val : {} / date : {}\n".format(*elm)) # Insert request instead !
			curs.execute("INSERT INTO data VALUES(NULL,{},{},{},{}".format(self.currentRideId, elm[0], elm[1], datetime.datetime.fromtimestamp(int(elm[2])).strftime('%Y-%m-%d %H:%M:%S')))

		#self.insertData(msg.endOfRideRequest.element)

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
		
		now = datetime.datetime.now()

		curs.execute("UPDATE ride SET start_date = '{}' WHERE id = {}".format(now.strftime('%Y-%m-%d %H:%M:%S'), self.currentRideId))

		voltage = 240
		for j in range(3600) : 
			speed = round(random.uniform(20,30)*(math.sin(j*0.01)+1),2)
			intensity = round(speed/10,2)

			curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.currentRideId,1,speed,now.strftime('%Y-%m-%d %H:%M:%S')))
			curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.currentRideId,2,voltage,now.strftime('%Y-%m-%d %H:%M:%S')))
			curs.execute("INSERT INTO data VALUES (NULL, {}, {} , {}, '{}')".format(self.currentRideId,3,intensity,now.strftime('%Y-%m-%d %H:%M:%S')))

			now += datetime.timedelta(0,1)

			voltage = round(voltage-0.04,2)

		curs.execute("UPDATE ride SET end_date = '{}' WHERE id = {}".format(now.strftime('%Y-%m-%d %H:%M:%S'), self.currentRideId))
		
		curs.close()
		self.mydb.commit()


	def setCurrentRide(self, rideId) :
		self.currentRideId = rideId;

	def addElement(self, element, table, row) :
		curs = self.mydb.cursor(dictionary=True)

		curs.execute("SHOW columns FROM {}".format(table))

		result = curs.fetchall()

		for column in result :
			setattr(element, column["Field"], str(row[column["Field"]]))

		curs.close()

	def generateDataMsg(self) :
		self.resetDbConnection()

		curs = self.mydb.cursor(dictionary=True)

		print("SELECT end_date from ride where id={}".format(self.currentRideId))

		curs.execute("SELECT end_date from ride where id={}".format(self.currentRideId))

		result = curs.fetchone()

		msg = synchro_pb2.CarToServ()
		msg.endOfRideRequest.Clear()

		msg.endOfRideRequest.id = self.currentRideId
		msg.endOfRideRequest.endDate =  result["end_date"].strftime('%Y-%m-%d %H:%M:%S')

		table = "data"

		curs.execute("SELECT measure_id, value, added_on FROM {}".format(table))

		result = curs.fetchall()

		mystr = "["

		for row in result :
			mystr+="{{{},{},{}}},".format(row["measure_id"] ,row["value"], int(row["added_on"].timestamp()))

		mystr = mystr[:-1] + "]"

		mystrCompress = lzma.compress(mystr.encode('utf_8'))

		msg.endOfRideRequest.data = mystrCompress

		curs.close()

		return msg.SerializeToString()

	def generateData(self) :
		self.insertFakeData()
		msg = self.generateDataMsg()

		print(msg)

		return msg.SerializeToString()


	def startRide(self) :
		msg = synchro_pb2.CarToServ()
		msg.startOfRideRequest.id=self.currentRideId
		msg.startOfRideRequest.startDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		return msg.SerializeToString()

	def setStartRide(self, msg) :
		curs = self.mydb.cursor()

		self.currentRideId = msg.startOfRideRequest.id

		curs.execute("UPDATE ride SET start_date='{}' WHERE id='{}'".format(msg.startOfRideRequest.startDate, self.currentRideId))

		curs.close()
		self.mydb.commit()

		resp = synchro_pb2.ServToCar()
		resp.startOfRideResponse.taskDone = True
		return resp.SerializeToString()

	def generateDataResp(self) :
		msg = synchro_pb2.ServToCar()
		msg.endOfRideResponse.taskDone = True
		return msg.SerializeToString()

	def isTaskDone(self, msg) :
		msg = synchro_pb2.ServToCar.FromString(msg)

		if msg.HasField("startOfRideResponse") :
			if msg.startOfRideResponse.taskDone == True :
				return True
			else :
				return False
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
	