# Flask-Bet-Mysql


### This is a Flask web application that allows users to place bets on different matches and keep track of their bets. The application uses a MySQL database to store user information and bet details.


## Docker Build
### To build the Docker image for this application, run the following command in the project directory:
```
docker build -t bet_flask .
```
### This will create a Docker image with the tag bet_flask.

## Docker Compose

### To start the application using Docker Compose, run the following command in the project directory:

'''
docker-compose up
'''

### This will start the application and its dependencies (i.e., the MySQL database) in separate Docker containers.


### After starting the application, you can access it by navigating to http://localhost:5000 in your web browser. From there, you can create an account, log in, and place bets on different matches.

## Additional Features
### Data is obtained from odds with an asynchronous request in the API.
### Twilio is used to send messages in WhatsApp with information about bets.
