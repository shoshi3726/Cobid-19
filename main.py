

import matplotlib.pyplot as plt

import io
from flask import Flask, jsonify, request, Response, send_file, url_for, render_template,send_from_directory
import pandas as pd

from datetime import datetime, timedelta

import datetime
import os

from werkzeug.utils import secure_filename


def is_valid_date(date_str):
    try:
        # check if the string is a valid date in one of the supported formats
        date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
    except ValueError:
        try:
            date = datetime.datetime.strptime(date_str, '%d-%m-%Y')
        except ValueError:
            return False

    # check if the date is within the desired range
    min_date = datetime.datetime.strptime('01/01/1900', '%d/%m/%Y')
    max_date = datetime.datetime.now()
    return min_date <= date <= max_date


def vaccinationDatesValid(a, b):
    try:
        # check if the string is a valid date in one of the supported formats
        first = datetime.datetime.strptime(a, '%d/%m/%Y')
        second = datetime.datetime.strptime(b, '%d/%m/%Y')
    except ValueError:
        try:
            first = datetime.datetime.strptime(a, '%d-%m-%Y')
            second = datetime.datetime.strptime(a, '%d-%m-%Y')
        except ValueError:
            return False

    # check if the date is within the desired range
    min_date = datetime.datetime.strptime('01/03/2020', '%d/%m/%Y')
    max_date = datetime.datetime.now()
    return min_date <= first < second <= max_date


app = Flask(__name__)


# endpoint to get all records from the clientDf
@app.route('/get_record')
def get_record():
    df = pd.read_csv('userDetails.csv')
    vaccination = pd.read_csv('vaccination.csv')

    record_df = df.loc[df['ID'] == int(request.args.get('ID'))]
    covidDetails_df = vaccination.loc[vaccination['ID'] == int(request.args.get('ID'))]
    if record_df.empty:
        return jsonify({'error': 'Client not found.'}), 404
    record = record_df.to_dict(orient='records')[0]
    # add message to the response
    response = {'message': 'The details of the ID card you submitted are:', 'record': record}


    if covidDetails_df.empty:
        return jsonify(response), 200
    covid_details = covidDetails_df.to_dict(orient='records')[0]
    response_covid = {'message': 'The details of covid of the ID card you submitted are:', 'covid': covid_details}
    response_covid.update(response)
    return jsonify(response_covid), 200


# Endpoint to insert a new record
@app.route('/insert', methods=['POST'])
def insert_record():
    df = pd.read_csv('userDetails.csv')
    vaccination = pd.read_csv('vaccination.csv')

    data = request.get_json()

    user_record = data['user_details']
    for key, value in user_record.items():
        if value == '' or value is None:
            return jsonify({'error': f'{key} cannot be empty.'}), 400
    vaccination_record = data['vaccination_details']

    id_number = user_record['ID']
    home_phone = user_record['home_phone_number']
    phone_number = user_record['phone_number']
    date = user_record['birthdate']

    # check if ID contains only digits
    if not (id_number.isdigit() and len(id_number) == 9):
        return jsonify({'error': 'Invalid ID number.'}), 400
    # check if ID already exists
    if str(id_number) in df['ID'].astype(str).values:
        return jsonify({'error': 'ID number already exists.'}), 400
    if not (home_phone.isdigit() or len(home_phone) != 9 or home_phone[0] != 0):
        return jsonify({'error': 'Invalid home phone number.'}), 400
    if not (phone_number.isdigit() or len(phone_number) != 10 or phone_number[:2] != "05"):
        return jsonify({'error': 'Invalid phone number.'}), 400
    if not is_valid_date(date):
        return jsonify({'error': 'Invalid birthdate.'}), 400


    #print(vaccination_record)
    for key, value in vaccination_record.items():
        if value == '' or value is None:
            return jsonify({'message': f'{key} cannot be empty. Only user detailes has been entered and not covid details'})
        else:
            m1 = vaccination_record['Manufacturer of First Vaccination']
            m2 = vaccination_record['Manufacturer of Second Vaccination']
            m3 = vaccination_record['Manufacturer of Third Vaccination']
            m4 = vaccination_record['Manufacturer of Fourth Vaccination']

            first_vaccine_date = vaccination_record['Date of First Vaccination']
            second_vaccine_date = vaccination_record['Date of Second Vaccination']
            third_vaccine_date =vaccination_record['Date of Third Vaccination']
            fourth_vaccine_date = vaccination_record['Date of Fourth Vaccination']

            # Convert start date and recovery date to datetime objects
            start_date = vaccination_record['Start Date']
            recovery_date = vaccination_record['Recovery Date']

            #If not all of the manufacturers are the same
            if not (m1==m2==m3==m4):
                return jsonify({'error': 'Invalid Manufacturer of Vaccination'}), 400

            if not (vaccinationDatesValid(first_vaccine_date, second_vaccine_date) \
                    and vaccinationDatesValid(second_vaccine_date, third_vaccine_date) \
                    and vaccinationDatesValid(third_vaccine_date, fourth_vaccine_date)):
                return jsonify({'error': 'Invalid vaccination date'}), 400
            # Check if recovery date is after start date
            if vaccinationDatesValid(recovery_date, start_date):
                return jsonify({'error': 'Recovery date is invalid'}), 400

            df.loc[len(df)] = user_record
            # save the data frame to file
            df.to_csv('userDetails.csv', index=False)
            vaccination.loc[len(vaccination)] = vaccination_record
            vaccination.to_csv('vaccination.csv', index=False)
            return jsonify({'message': 'Record inserted successfully'})


@app.route('/insertPersonalDetails', methods=['POST'])
def insert_personal_details():
    df = pd.read_csv('userDetails.csv')

    user_record = request.get_json()

    for key, value in user_record.items():
        if value == '' or value is None:
            return jsonify({'error': f'{key} cannot be empty.'}), 400

    id_number = user_record['ID']
    home_phone = user_record['home_phone_number']
    phone_number = user_record['phone_number']
    date = user_record['birthdate']

    # check if ID contains only digits
    if not (id_number.isdigit() and len(id_number) == 9):
        return jsonify({'error': 'Invalid ID number.'}), 400
    # check if ID already exists
    if str(id_number) in df['ID'].astype(str).values:
        return jsonify({'error': 'ID number already exists.'}), 400
    if not (home_phone.isdigit() or len(home_phone) != 9 or home_phone[0] != 0):
        return jsonify({'error': 'Invalid home phone number.'}), 400
    if not (phone_number.isdigit() or len(phone_number) != 10 or phone_number[:2] != "05"):
        return jsonify({'error': 'Invalid phone number.'}), 400
    if not is_valid_date(date):
        return jsonify({'error': 'Invalid birthdate.'}), 400
    df.loc[len(df)] = user_record
    # save the data frame to file
    df.to_csv('userDetails.csv', index=False)
    return jsonify({'message': 'Only user details have been inserted'})

@app.route('/insertVaccinationsDetails', methods=['POST'])
def insert_vaccinations_details():
    df = pd.read_csv('userDetails.csv')
    vaccination = pd.read_csv('vaccination.csv')

    vaccination_record = request.get_json()
    id = vaccination_record['ID']
    if str(id) not in str(df['ID'].values):
        return jsonify({'error': 'Invalid ID, The client is not a member of a health fund'})
    if str(id) in str(vaccination['ID'].values):
        return jsonify({'error': 'Invalid ID, The client vaccinations details already exists'})

    for key, value in vaccination_record.items():
        if value == '' or value is None:
            return jsonify({'message': f'{key} cannot be empty.'})
        else:
            m1 = vaccination_record['Manufacturer of First Vaccination']
            m2 = vaccination_record['Manufacturer of Second Vaccination']
            m3 = vaccination_record['Manufacturer of Third Vaccination']
            m4 = vaccination_record['Manufacturer of Fourth Vaccination']
            #print(m1,m2,m3,m4)

            first_vaccine_date = vaccination_record['Date of First Vaccination']
            second_vaccine_date = vaccination_record['Date of Second Vaccination']
            third_vaccine_date =vaccination_record['Date of Third Vaccination']
            fourth_vaccine_date = vaccination_record['Date of Fourth Vaccination']

            # Convert start date and recovery date to datetime objects
            start_date = vaccination_record['Start Date']
            recovery_date = vaccination_record['Recovery Date']

            #If not all of the manufacturers are the same
            if not (m1==m2==m3==m4):
                return jsonify({'error': 'Invalid Manufacturer of Vaccination'}), 400

            if not (vaccinationDatesValid(first_vaccine_date, second_vaccine_date) \
                    and vaccinationDatesValid(second_vaccine_date, third_vaccine_date) \
                    and vaccinationDatesValid(third_vaccine_date, fourth_vaccine_date)):
                return jsonify({'error': 'Invalid vaccination date'}), 400
            # Check if recovery date is after start date
            if vaccinationDatesValid(recovery_date, start_date):
                return jsonify({'error': 'Recovery date is invalid'}), 400
            vaccination.loc[len(vaccination)] = vaccination_record
            vaccination.to_csv('vaccination.csv', index=False)
            return jsonify({'message': 'Record of vacinations inserted successfully'})

@app.route('/api/sick_patients_last_month', methods=['GET'])
def get_sick_patients_last_month():
    vaccination = pd.read_csv('vaccination.csv')
    try:
        # Get the current date and the date one month ago
        today = datetime.datetime.now().date()
        one_month_ago = today - timedelta(days=30)

        # Filter the DataFrame to only include patients who started treatment in the last month
        filtered_df = vaccination[(pd.to_datetime(vaccination['Start Date'], format='%d/%m/%Y').dt.date >= one_month_ago) &
                                   (pd.to_datetime(vaccination['Start Date'], format='%d/%m/%Y').dt.date <= today)]

        # Create a dictionary to hold the count of patients for each day of the last month
        count_dict = {}
        for i in range((today - one_month_ago).days + 1):
            count_dict[str(one_month_ago + timedelta(days=i))] = 0

        # Count the number of patients for each day in the filtered DataFrame
        for start_date in filtered_df['Start Date']:
            start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y').date()
            if start_date >= one_month_ago and start_date <= today:
                count_dict[str(start_date)] += 1

        # Create a list of x and y values for the plot
        x = list(count_dict.keys())
        y = list(count_dict.values())

        # Generate the plot as a bar chart
        plt.bar(x, y)
        plt.xlabel('Date')
        plt.ylabel('Number of Patients')
        plt.title('Number of Patients Who Started Treatment in the Last Month')
        plt.xticks(rotation=45)

        # Save the plot as a PNG file
        #plt.savefig('patient_data.png')
        #return jsonify({'message': 'Patient data generated successfully.'}), 200

        # Save the plot as a PNG file in memory
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        img_bytes.seek(0)

        # Return the image data to the client
        return send_file(img_bytes, mimetype='image/png')

    except Exception as e:
        result = f"Failed to generate patient data: {str(e)}"
        return jsonify({'error': result}), 500



@app.route('/api/members_who_didnt_get_vaccinated')
def members_who_didnt_get_vaccinated():
    df = pd.read_csv('userDetails.csv')
    vaccination = pd.read_csv('vaccination.csv')

    non_vaccinated = df[~(df['ID'].isin(vaccination['ID']))]
    return (f"The number of members in the health fund who have not yet been vaccinated is:: {len(non_vaccinated)}")


UPLOAD_FOLDER = 'C:/Users/1/Desktop/pythonProject'  # Change this to the desired folder path
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Set the allowed file extensions

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/api/add_user_picture', methods=['POST'])
def add_user_picture():
    df = pd.read_csv('userDetails.csv')
    id = request.form['ID']
    if str(id) not in str(df['ID'].values):
        return jsonify({'error': 'Invalid user ID'})

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(f'File saved as: {filename}')

        # Add the filename to the user details dataframe
        df.loc[df['ID'].astype(str) == str(id), 'picture'] = filename
        df.to_csv('userDetails.csv', index=False)

        return jsonify({'message': 'Picture added successfully'})
    else:
        return jsonify({'error': 'Invalid file format'})




if __name__ == '__main__':
    app.run(debug=True)
