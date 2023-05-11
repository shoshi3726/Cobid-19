
import requests

user_details = {
    'name': 'Roni',
    'ID': '188989255',
    'city': 'tel aviv',
    'street': 'Shibuya',
    'house_number': '7',
    'birthdate': '22/06/1995',
    'home_phone_number': '555-6789',
    'phone_number': '555-5555'
}

vaccination_details = {
    'Date of First Vaccination': '01/05/2022',
    'Manufacturer of First Vaccination': 'Moderna',
    'Date of Second Vaccination': '22/05/2022',
    'Manufacturer of Second Vaccination': 'Moderna',
    'Date of Third Vaccination': '24/05/2022',
    'Manufacturer of Third Vaccination': 'Moderna',
    'Date of Fourth Vaccination': '25/05/2022',
    'Manufacturer of Fourth Vaccination': 'Moderna',
    'Start Date': '01/05/2023',
    'Recovery Date': '29/06/2023'
}

record = {
    'user_details': user_details,
    'vaccination_details': {'ID': user_details['ID'],
                            **vaccination_details}

}

response = requests.post('http://localhost:5000/insert', json=record)
print(response.json())  # {'message': 'Record inserted successfully'}

