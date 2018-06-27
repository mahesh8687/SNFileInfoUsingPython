# Set the request parameters
table_name = 'x_26916_file_info_u_file_info'
base_url = 'https://<yourinstance>.service-now.com'
user = ''
pwd = ''
input_directory = 'C:\\Users\\<name>\\Downloads'
	
def create_record(input_json):
	#Need to install requests package for python
	#easy_install requests
	import requests

	# Set proper headers
	headers = {"Content-Type":"application/json","Accept":"application/json"}

	url = base_url + '/api/now/table/' + table_name
	# Do the HTTP request
	response = requests.post(url, auth=(user, pwd), headers=headers ,data=str(input_json))

	# Check for HTTP codes other than 201
	if response.status_code != 201: 
		print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
		#exit()

	# Decode the JSON response into a dictionary and use the data
	data = response.json()
	return data

	
def send_file_content(folderName, filename, table_sys_id):
	#Need to install requests package for python
	#easy_install requests
	import requests

	# Set proper headers
	headers = {"Content-Type":"application/json","Accept":"application/json"}

	url = base_url + '/api/now/attachment/file?table_name=' + table_name + '&table_sys_id=' + table_sys_id + '&file_name=' + filename

	print(url)
	data = open(folderName + "/" + filename, 'rb').read()
	# Do the HTTP request
	response = requests.post(url, auth=(user, pwd), headers=headers ,data=data)

	# Check for HTTP codes other than 201
	if response.status_code != 201: 
		print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
		#exit()

	# Decode the JSON response into a dictionary and use the data
	data = response.json()
	return data
	
	

def scan_files_in_folder():
	import os
	import mimetypes
	
	for folderName, subfolders, filenames in os.walk(input_directory):
		for filename in filenames:
			print('FILE INSIDE ' + folderName + ': '+ filename)
			input_json = dict()
			input_json["file_name"] = filename
			input_json["path"] = folderName
			input_json["size"] = os.path.getsize(folderName + "/" + filename)
			input_json["content_type"] = mimetypes.guess_type(folderName + "/" + filename)[0]
			

			#print(input_json)
			record = create_record(input_json)
			table_sys_id = record["result"]["sys_id"]
			print(record)
			
			send_file_content(folderName, filename, table_sys_id)
			
	


	
scan_files_in_folder()

