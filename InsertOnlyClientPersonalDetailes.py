import requests

user_details = {
    'name': 'Roni',
    'ID': '188979256',
    'city': 'tel aviv',
    'street': 'Shibuya',
    'house_number': '7',
    'birthdate': '22/06/1995',
    'home_phone_number': '555-6789',
    'phone_number': '555-5555'
}

response = requests.post('http://localhost:5000/insertPersonalDetails', json=user_details)
print(response.json())