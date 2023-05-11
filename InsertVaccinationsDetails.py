import requests
vaccination_details = {
    'ID': '188979256',
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
response = requests.post('http://localhost:5000/insertVaccinationsDetails', json=vaccination_details)
print(response.json())  # {'message': 'Record inserted successfully'}
