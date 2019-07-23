

from time import time, sleep






class User():
	_priority= 1
	def __init__(s, gl, se, con, addr):
		gl.all_priorities+= s._priority

		s.gl= gl
		s.se= se
		s.con= con
		s.ip, s.port= addr


	def recvb(s, amount):
		recived= b""
		while amount:
			priority= s._priority/ s.gl.all_priorities
			max_download= int(s.se.global_download_limit* priority)

			if max_download <= amount:
				to_download= max_download
				amount-= max_download
			else:
				to_download= amount
				amount= 0

			recived+= s.con.recv(to_download)

			sleep(to_download/ max_download)
		return recived

	def sendallb(s, data):
		while data:
			priority= s._priority/ s.gl.all_priorities
			max_upload= int(s.se.global_upload_limit* priority)

			to_upload= data[:max_upload]
			data= data[max_upload:]
			s.con.sendall(to_upload)

			sleep(len(to_upload)/ max_upload)


	def recive_header(s):
		start= time()
		data= b""
		while 1:
			if start+s.se.time_to_recive_header < time():
				raise TimeoutError("header not sent in time")

			remains= s.se.header_maxlen - len(data)
			bit= s.recvb(1)

			data+= bit
			if data.endswith(b"\r\n"):
				del start
				del remains
				del bit

				data= data[:-2]
				break

		data= data.decode()#decode error
		header= data.split(" ")
		del data
		if len(header)!=3:
			raise ValueError("header's format is bad")
		s.meth, s.url, s.proto= header#... da opravq url-a i dekodiraneto


	def recive_body(s):
		start= time()
		data= b""
		while 1:
			if start+s.se.time_to_recive_body < time():
				raise TimeoutError("body not sent in time")

			remains= s.se.body_maxlen- len(data)
			if remains<=0:
				raise ValueError("body is too long")
			frame= s.recvb(remains)

			data+= frame
			if data.endswith(b"\r\n\r\n"):
				del start
				del remains
				del frame

				data= data[:-4]
				break

		data= data.decode()#decode error
		body= {}
		for line in data.split("\r\n"):
			if ": " in line:
				ind= line.index(": ")
				key= line[:ind]
				value= line[ind+2:]
				body[key]= value
		del data

		coo= {}
		if "Cookie" in body:
			for line in body["Cookie"].split("; "):
				if "=" in line:
					ind= line.index("=")
					key= line[:ind]
					value= line[ind+1:]
					coo[key]= value
				else:
					coo[line]= ""
			del body["Cookie"]

		s.body= body
		s.coo= coo


	def send_file(s, dir):
		f= open(dir, "rb")
		while 1:
			chunk= s.se.file_sending_chunk
			to_send= f.read(chunk)
			if to_send==b"":
				break
			s.sendallb(to_send)
			if len(to_send)< chunk:
				break
		f.close()








	def change_priotiry(s, new):
		change= new- s._priority
		s.gl.all_priorities+= change
		s._priority= new

	def __del__(s):
		s.gl.all_priorities-= s._priority