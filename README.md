# Cobid-19
Health fund management system in Corona.

The system handles entering member data into the health insurance system, and in addition, according to the ID, the system will display the member's details, and his details regarding Corona and vaccinations.

In the main file there are the functions:

@app.route('/get_record')
This function receives an ID from the client and prints his personal information and information regarding vaccinations
Access to the function is via 'http://localhost:5000/get_record?ID=id_number'

@app.route('/insert', methods=['POST'])
This function enters a member's details and his vaccination details
Insertion is done using the request file 'InsertClientAndVaccinationDetails'

@app.route('/insertPersonalDetails', methods=['POST'])
This function only enters the user's personal information
Insertion is done using the request file 'InsertOnlyClientPersonalDetails'

@app.route('/insertVaccinationsDetails', methods=['POST'])
This function only enters the user's immunization information
Insertion is done using the request file 'InsertVaccinationsDetails'

@app.route('/api/sick_patients_last_month', methods=['GET'])
This function prints to the user a graph that shows the number of patients on each day of the last month. The call to the function is via 'http://localhost:5000/api/sick_patients_last_month'

@app.route('/api/members_who_didnt_get_vaccinated')
This function prints the number of patients in the register who were not vaccinated. The function is called using 'http://localhost:5000/api/members_who_didnt_get_vaccinated'

@app.route('/api/add_user_picture', methods=['POST'])
The function adds an image to the user's personal details.
The insertion is done using the request file 'InsertImageClient'
