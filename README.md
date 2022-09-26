Project Title: GlueReply API technical task
Coded by: James Hayes O'Brien
Date: 2022-09-26

During this project I built my first API using Python and Flask.
Under GlueAPI\main.py the main python file can be found. I have not seperated unit tests into a seperate file. The unit tests I have written effectively validate the correctness of the validations carried out on various incoming JSON data. I wasn't able to write unit tests that validated the HTTP responses, so for this, I thoroughly tested the project using POSTMAN.

Python packages such as Flask will need to be installed before this project can run.

Upon execution, this API will run on port 127.0.0.1:5000. There is no "home" or "default" endpoint. 
Endpoint /users accepts "GET" and "POST" requests, endpoint /payments accepts only "POST" requests.

To observe the functionality of this API, configure your API platform to http://127.0.0.1:5000 and specify one of the available endpoints.

The following script of requests can be followed to observe program effectiveness:
-> http://127.0.0.1:5000/users POST {
    "Username": "Student1",
    "Password": "Password1",
    "Email": "jhayesobrien@gmail.com",
    "DoB": "2000-06-05",
    "Credit Card Number": "0123456789012345"
}
-> http://127.0.0.1:5000/users POST {
    "Username": "jhayesobrien1",
    "Password": "Password1",
    "Email": "jhayesobrien@gmail.com",
    "DoB": "2000-06-05",
    "Credit Card Number": "0123456789012346"
}
-> http://127.0.0.1:5000/users POST {
    "Username": "jhayesobrienN0bank",
    "Password": "Password1",
    "Email": "jhayesobrien@gmail.com",
    "DoB": "2000-06-05"}
-> http://127.0.0.1:5000/payments POST {
    "Credit Card Number": "0123456789012345",
    "Amount": "200"
}	# will respond with "Payment Request Successful", status 201

-> http://127.0.0.1:5000/users GET
	# will return the three previously POSTed users

-> http://127.0.0.1:5000/users?CreditCard=Yes GET
	# will return users with credit card number



To execute the prewritten unit tests, open the python file, comment out "app.run()" and uncomment "unittest.main()". Run the program.
