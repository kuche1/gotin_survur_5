

class Settings():
	response_file_dir= "response"

	using_ssl= True
	ssl_key_dir= "certificate\\private.key"
	ssl_cert_dir= "certificate\\selfsigned.crt"
	ssl_version= __import__("ssl").PROTOCOL_SSLv23

	host= ""
	port= 443 if using_ssl else 80
	listen= 5

	max_running_threads= 8
	reload_user_class_on_every_new_connection= True
	reload_response_on_every_new_connection= True
	save_errors_in_log= True #...
	raise_errors_in_console= True

	time_to_recive_header= 4
	header_maxlen= 80
	time_to_recive_body= 16
	body_maxlen= 2048

	global_download_limit= 1024*1024* 1
	global_upload_limit= 1024*1024* 3

	file_sending_chunk= 2048
