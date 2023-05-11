
import pandas as pd


# Create an empty DataFrame
# initialize the dataframe with the desired columns
data = {'name': ['Alice', 'Bob', 'Charlie'],
        'ID': ['123333333', '456666666','777777777' ],
        'city': ['New York', 'Paris', 'London'],
        'street': ['Broadway', 'Champs-Élysées', 'Baker Street'],
        'house_number': [10, 20, 30],
        'birthdate': ['1990-01-01', '1980-02-02', '1970-03-03'],
        'home_phone_number': ['111-111-1111', '222-222-2222', '333-333-3333'],
        'phone_number': ['444-444-4444', '555-555-5555', '666-666-6666']}

df = pd.DataFrame(data)

vaccination = pd.DataFrame({
    'ID': ['123333333', '456666666', '777777777'],
    'Date of First Vaccination': ['01/04/2021', '15/05/2021', '30/06/2021'],
    'Manufacturer of First Vaccination': ['Pfizer', 'Moderna', 'AstraZeneca'],
    'Date of Second Vaccination': ['22/04/2021', '09/06/2021', '28/07/2021'],
    'Manufacturer of Second Vaccination': ['Pfizer', 'Moderna', 'AstraZeneca'],
    'Date of Third Vaccination': ['13/05/2021', '30/06/2021', '18/08/2021'],
    'Manufacturer of Third Vaccination': ['Pfizer', 'Moderna', 'AstraZeneca'],
    'Date of Fourth Vaccination': ['03/06/2021', '21/07/2021', '07/09/2021'],
    'Manufacturer of Fourth Vaccination': ['Pfizer', 'Moderna', 'AstraZeneca'],
    'Start Date': ['15/03/2021', '01/04/2021', '15/05/2021'],
    'Recovery Date': ['01/04/2021', '15/04/2021', '01/06/2021']
})
df.to_csv('userDetails.csv', index=False)
vaccination.to_csv('vaccination.csv',index=False)
