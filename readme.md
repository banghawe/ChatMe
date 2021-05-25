# ChatMe - Live Chat Application

ChatMe is live chat application was built using django, django-channel and redis.
ChatMe using websocket to support realtime chat

# Getting Started

## How to run project on local environment

1. Please install docker on your machine
2. Create .env file based on .env.example
3. Running
   ```console
   docker-compose up --build
   ```
4. Run backend terminal and run next instruction on chatme-backend terminal
   ```console
   docker-compose run chatme-backend sh
   ```
5. Migrate db schemes
   ```console
   python manage.py migrate
   ```
6. Add superuser for django admin
   ```console
   python manage.py createsuperuser
   ```
   and follow the instructions
7. Run test
   ```console
   coverage run --omit --source='.' manage.py test
   ```
   
## How to test chatme using Postman

You can test websocket using Postman 8.5

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/5874517-99c2d11a-79ae-49f3-9f01-3dbcc91d849f?action=collection%2Ffork&collection-url=entityId%3D5874517-99c2d11a-79ae-49f3-9f01-3dbcc91d849f%26entityType%3Dcollection%26workspaceId%3D283b3077-698c-4d12-9ebc-dc8b20844ab5)

1. Connect to ws
   ![connect to ws](https://i.imgur.com/nl6wR1a.png)
2. Send message through API
   Endpoint: 
   http://localhost:8000/message/:session_code
   ![send message API](https://i.imgur.com/Jj1X7al.png)
3. Receive message through websocket, connect to
   ws://localhost:8000/:session_code
   ![Receive message](https://i.imgur.com/iZyLZjM.png)