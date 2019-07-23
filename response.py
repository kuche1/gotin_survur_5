







def response(u):
	u.recive_header()
	print(u.meth)
	print(u.ip)
	#print(u.url)
	#print(u.proto)
	u.recive_body()
	print(u.body)
	print(u.coo)

	u.sendallb(b"kur")
