import socket
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ip = '192.168.0.144' #define who we're talking to (matches Arduino's IP and port)
port = 5010

sock.bind(('', port))

sock.settimeout(1) #wait only 1 sec for response



Base = declarative_base()
class Entry(Base):
	__tablename__ = "d1"
	id = Column('id', Integer, primary_key=True)
	sensor_id = Column('sensor', Integer)
	timestamp = Column('timestamp', DateTime)
	temperature = Column('temperature', Float)
	pressure = Column('pressure', Float)
	no2 = Column('no2', Float)

with open("url.txt", 'r') as file:
	url = file.read()

engine = create_engine(url, echo=True) #url in the form mysql+pymysql://username:password@host:port/database

Base.metadata.create_all(bind=engine)

def add_entry(list_data:list):
	Session = sessionmaker(bind=engine)
	session = Session()
	entry = Entry()

	entry.sensor_id = list_data[0]
	entry.timestamp = datetime.datetime.now()
	entry.temperature = list_data[1]
	entry.pressure = list_data[2]
	entry.no2 = list_data[3]
	session.add(entry)
	session.commit()

	session.close()

while (1):
	request = b"Data"
	
	try:
		sock.sendto(request, (ip, port)) #send command to Arduino
		received_data, addr = sock.recvfrom(2048) #read response from Arduino
		print("Received: {}" .format(received_data))
		received_data = received_data.decode("utf-8")
		list_data = received_data.split(',')
		print(list_data)
		add_entry(list_data)
	except:
		print("didn't work")

	
	time.sleep(8)
