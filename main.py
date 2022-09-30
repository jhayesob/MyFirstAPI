import json
import re
from datetime import datetime, date
from flask import Flask, Response, request
import unittest

app = Flask(__name__)

users = []   # In-program variable to store user data. No need for DB on this specific project


def username_valid(username_str):
    # checking if incoming username data is of valid format: ensuring string is alphanumeric and not containing spaces
    if ' ' not in username_str and username_str.isalnum():
        return True
    else:
        return False


def username_already_exists(username_str):
    # checking if a username comprising the same string as the incoming data already exists in program data
    # loops through all current users, checks their name against incoming string.
    for usr in users:
        if usr['Username'] == username_str:
            return True
    return False


def password_valid_format(password_str):
    # checking if newly entered password string contains appropriate number of uppercase, digit and lowercase chars.
    # python regular expression notation used to check string
    password_regex = r'^(?=.*?[A-Z])(?=.*?[0-9]).{8,}$'
    if len(password_str) >= 8 and re.fullmatch(password_regex, password_str):
        return True
    else:
        return False


def email_valid(email_str):
    # checking if newly entered email string is in a valid email format
    # python regular expression notation used to check string
    email_regex_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(email_regex_pattern, email_str):
        return True
    else:
        return False


def dob_valid_format(dob_str):
    # check: is Date of Birth supplied in correct ISO format
    # ISO format = yyyy-mm-dd
    # Python features in built functions to support this operation
    try:
        datetime.fromisoformat(dob_str)  # .replace('Z', '+00:00')
    except:  # should provide exact form of exception that would be thrown
        return False
    return True


def age_over_18(dob):
    # check: using provided user DoB, is their age above 18?

    # in-build modules exist for this type of operation, but for fear of errors surrounding leap years, a more
    # bare-bones approach was implemented

    now = datetime.now()
    date_today = now.strftime("%Y-%m-%d")
    if int(date_today[:4]) - int(dob[:4]) > 18:
        return True
    elif int(date_today[:4]) - int(dob[:4]) == 18:
        if int(date_today[5:7]) > int(dob[5:7]):
            return True
        elif int(date_today[5:7]) == int(dob[5:7]):
            if int(date_today[8:10]) >= int(dob[8:10]):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def card_valid(card_str):
    if card_str.isnumeric() and len(card_str) == 16:
        return True
    else:
        return False


@app.route('/users', methods=['POST'])
def registration_service():
    print('users POST request made')
    data = request.get_json()
    if not username_valid(data['Username']) or not password_valid_format(data['Password']) or not \
            email_valid(data['Email']) or not dob_valid_format(data['DoB']):
        return Response('Request rejected: failed to satisfy one or more basic validation checks', status=400)
    if "Credit Card Number" in data.keys():
        if not card_valid(data['Credit Card Number']):
            return Response('Request rejected: failed to satisfy one or more basic validation checks', status=400)
    if username_already_exists(data['Username']):
        return Response('Request rejected: Username already exists in program', status=409)
    if not age_over_18(data['DoB']):
        return Response('Request rejected: age below 18', status=403)

    if 'Credit Card Number' in data.keys():
        users.append(
            {
                'Username': data['Username'],
                'Password': data['Password'],
                'Email': data['Email'],
                'DoB': data['DoB'],
                'Credit Card Number': data['Credit Card Number']
            }
        )
    else:
        users.append(
            {
                'Username': data['Username'],
                'Password': data['Password'],
                'Email': data['Email'],
                'DoB': data['DoB']
            }
        )
    return Response('Data Accepted', status=201)


@app.route('/users', methods=['GET'])
def get_user_details():
    print('users get request made')
    # how do I pass the filter in this request - python flask path parameter
    filter_args = request.args
    ret_str = ""
    if 'CreditCard' in filter_args.keys():
        if filter_args['CreditCard'] == 'Yes':
            for usr in users:
                if 'Credit Card Number' in usr.keys():
                    ret_str = ret_str + json.dumps(usr) + "\n"
        elif filter_args['CreditCard'] == 'No':
            for usr in users:
                if 'Credit Card Number' not in usr.keys():
                    ret_str = ret_str + json.dumps(usr) + "\n"
    else:
        for usr in users:
            ret_str = ret_str + json.dumps(usr) + "\n"
    return Response(ret_str, status=201)


@app.route('/payments', methods=['POST'])
def payment_service():
    print('Payment post request made')
    data = request.get_json()

    if 'Credit Card Number' in data.keys():
        if not card_valid(data['Credit Card Number']):
            return Response('Request rejected: failed to satisfy one or more basic validation checks', status=400)

    if 'Amount' in data.keys():
        if not data['Amount'].isnumeric() or len(data['Amount']) != 3:
            return Response('Request rejected: failed to satisfy one or more basic validation checks', status=400)

    card_in_usr_data = False
    for usr in users:
        if 'Credit Card Number' in usr.keys():
            if usr['Credit Card Number'] == data['Credit Card Number']:
                card_in_usr_data = True

    if card_in_usr_data:
        return Response('Payment Request Successful', status=201)

    else:
        return Response('Request Rejected: Credit Card Number not in system', status=404)


class MyTestCases(unittest.TestCase):
    def test_username_valid(self):
        self.assertTrue(username_valid("Student1"))
        self.assertTrue(username_valid("Stu1"))
        self.assertTrue(username_valid("student1"))
        self.assertTrue(username_valid("student"))
        self.assertFalse(username_valid("Student 1"))

    def test_username_already_exists(self):
        users.append({'Username': 'James1'})
        self.assertTrue(username_already_exists("James1"))

    def test_password_valid_format(self):  # min length 8, 1 upper case, 1 number
        self.assertTrue(password_valid_format("Student1"))
        self.assertFalse(password_valid_format("james"))
        self.assertFalse(password_valid_format("james1"))
        self.assertFalse(password_valid_format("James1"))
        self.assertFalse(password_valid_format("18879990"))

    def test_email_valid(self):
        self.assertTrue(email_valid("jhayesobrien@gmail.com"))
        self.assertFalse(email_valid("johnsnow@gmail"))
        self.assertFalse(email_valid("anonymous123@uk"))
        self.assertFalse(email_valid("myemail@outlook."))

    def test_dob_valid_format(self):
        self.assertTrue(dob_valid_format("2000-06-05"))
        self.assertFalse(dob_valid_format("05-06-2000"))
        self.assertFalse(dob_valid_format("05062000"))  # don't know what this one is going to return

    def test_age_over_18(self):
        self.assertTrue(age_over_18("2004-09-26"))
        self.assertTrue(age_over_18("2004-09-20"))
        self.assertTrue(age_over_18("2004-08-26"))
        self.assertFalse(age_over_18("2004-11-01"))
        self.assertFalse(age_over_18("2005-01-01"))

    def test_card_valid(self):
        self.assertTrue(card_valid("0123456789012345"))
        self.assertFalse(card_valid("012345678901234"))
        self.assertFalse(card_valid("01234567890123456"))
        self.assertFalse(card_valid("01234567890123aa"))
        self.assertFalse(card_valid("01234567890123 a"))


if __name__ == '__main__':
    # unittest.main()  # in order to execute the written group of unit tests, uncomment this line. Unit tests have been
    # written to ensure the correct validation of incoming data
    app.run()
    # upon program execution, this API will run on port 127.0.0.1:5000
    # there is no homepage default endpoint. The /users endpoint accepts both GET and POST requests where endpoint
    # /payments accepts only POST requests.
