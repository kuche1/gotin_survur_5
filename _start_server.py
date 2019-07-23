

import ssl
import socket
import sys
import traceback
from threading import Thread

from cont_fl import imprt



def main(gl, se):
	
	if se.using_ssl:
		gl.sock = ssl.wrap_socket(gl.sock,server_side=True,do_handshake_on_connect=True,
			keyfile=se.ssl_key_dir, certfile=se.ssl_cert_dir,
			ssl_version=se.ssl_version
		)
	gl.sock.bind((se.host, se.port))
	gl.sock.listen(se.listen)

	gl.running_threads= se.max_running_threads
	for _ in range(se.max_running_threads):
		thread(handle_new_connections, (gl, se))


def handle_new_connections(gl, se):
	try:

		try:
			con, addr= gl.sock.accept()
		except ssl.SSLError:
			return#opitva da polzva http
		except OSError:
			return#samiq survur spira
		
		try:
			if se.reload_user_class_on_every_new_connection:
				gl.user_class= imprt("user").User
			
			User= gl.user_class
			u= User(gl, se, con, addr)

			if se.reload_response_on_every_new_connection:
				gl.response_fnc= imprt(se.response_file_dir).response 

			gl.response_fnc(u)
		finally:
			con.close()

	except:
		err_data = sys.exc_info()
		err_data= traceback.format_exception(*err_data)
		gl.errors.append( err_data )
		if se.raise_errors_in_console:
			raise

	finally:
		if gl.running:
			if gl.running_threads < se.max_running_threads:
				gl.running_threads += 1
				thread(handle_new_connections, (gl, se))
				thread(handle_new_connections, (gl, se))
			elif gl.running_threads == se.max_running_threads:
				thread(handle_new_connections, (gl, se))
			else:
				gl.running_threads -= 1
		else:
			gl.running_threads -= 1



def thread(fnc, args=(), kwargs={}):
	Thread(target=fnc, args=args, kwargs=kwargs).start()














def load_settings():
	return imprt("settings").Settings()


class Globals():
	def __init__(s, se):
		s.running= True
		s.sock= socket.socket()
		s.errors= []

		s.user_class= __import__("user").User
		s.all_priorities= 0

		s.response_fnc= __import__(se.response_file_dir).response


class UI():
	def __init__(s, gl, se):
		s.gl= gl
		s.se= se
	
	def stop_server(s):
		s.gl.running= False
		s.gl.sock.close()



if __name__ == "__main__":
	
	se= load_settings()
	gl= Globals(se)
	ui= UI(gl, se)

	main(gl, se)

	from code import interact
	interact(local=locals())