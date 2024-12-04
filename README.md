# Payment Web Service (Python)

## Prerequisites

* Python 3.10  
* PyCharm IDE (or any Python-compatible IDE)  
* XAMPP for phpMyAdmin

## Installation and Setup

1. **Install Python**   
* Download and install Python from the official Python website.

2. **Set Up Python Interpreter in PyCharm**  
* Open PyCharm.  
* Go to Settings → Python Interpreter.  
* Click Add Interpreter → Add Local Interpreter.  
* Choose Virtualenv Environment  
* Select Existing for Environment  
* Choose the interpreter that the path is same with project folder 

3. **Install Required Dependencies**  
* In PyCharm’s terminal, navigate to the project directory.  
* Run the following command to install dependencies:

  pip install \-r requirements.txt

4. **Database Setup**  
* Open phpMyAdmin from XAMPP.  
* Create a new database called **payment\_web\_service**.  
* Import the payment\_web\_service.sql file (in the git repository) into this database.

5. **Running the Service**  
* In PyCharm, click the Run button to run the app.py file (top right corner) to start the service.

### **Common Issues** 

1. **Database Connection Error:** 

* Make sure that xampp, mysql server is turn on
