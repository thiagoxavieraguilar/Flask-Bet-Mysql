# Flask-Bet-Mysql
# # This is a Flask web application that allows users to place bets on different events and keep track of their bets. The application uses a MySQL database to store user information and bet details.


# # Docker Build
# ## #To build the Docker image for this application, run the following command in the project directory:
```
docker build -t bet_flask .
```
# # # This will create a Docker image with the tag bet_flask.

# #Docker Compose
# # # To start the application using Docker Compose, run the following command in the project directory:
'''
docker-compose up
'''
# # # This will start the application and its dependencies (i.e., the MySQL database) in separate Docker containers.

# # Usage
# # # After starting the application, you can access it by navigating to http://localhost:5000 in your web browser. From there, you can create an account, log in, and place bets on different events.
