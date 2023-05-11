import requests

url = 'http://localhost:5000/api/add_user_picture'
filename  = 'C:/Users/1/Desktop/pythonProject/image.jpg' # Change this to the path of the image file you want to upload
id = '456666666' # Change this to the ID of the user you want to add the picture to

files = {'file': open(filename, 'rb')}
data = {'ID': id}

response = requests.post(url, files=files, data=data)

print(response.json())
