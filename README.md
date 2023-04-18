Flask-Bet-Mysql
This is a Flask web application that allows users to place bets on different events and keep track of their bets. The application uses a MySQL database to store user information and bet details.

Installation
To run this application, you will need Python 3.x and MySQL installed on your machine. Follow these steps to install the application:

Clone the repository:
bash
Copy code
git clone https://github.com/thiagoxavieraguilar/Flask-Bet-Mysql.git
Navigate to the project directory:
bash
Copy code
cd Flask-Bet-Mysql
Create a virtual environment:
Copy code
python3 -m venv venv
Activate the virtual environment:
bash
Copy code
source venv/bin/activate
Install the required packages:
Copy code
pip install -r requirements.txt
Set up the database:

Create a new MySQL database
Rename the config_sample.py file to config.py and update the database information
Run the application:

arduino
Copy code
python run.py
Usage
Once the application is running, you can access it in your web browser at http://localhost:5000. From there, you can register a new account, log in, and place bets on different events.
