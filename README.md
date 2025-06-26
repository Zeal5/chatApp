## Assumptions Made:
    - Signed In user can see all other registerd users
    - Signed In user can start conversation with all other users
    - User should only be allowed to send messages through a web interface while receiving and retrieving messages should be allowed through the REST API.


## CreateSuperUser:
    Either create superuser manually (using shell) or run `python manage.py runscript create_superuser` 
    and `python manage.py runscript create_superuser`
    This will create users with username a, b, c ... i and email a@a.com ... i@i.com

### Refer to [SETUP.md](https://github.com/Zeal5/chatApp/blob/master/SETUP.md) for setup instrustions
# Web Page Endpoints (Return HTML Templates)

## 1. Login/Signup Page
        URL: /

        Method: GET/POST

        View: login_or_signup

        Description: Handles user authentication (login/signup)

## 2. Logout
        URL: /logout/

        Method: GET

        View: user_logout

        Description: Logs out user


## 3. Chat Room
        URL: /chats/ or /chats/<room_name>/

        Method: GET

        View: chat_room

        Description: Renders chat interface


## 4. Start Chat
    URL: /chats/start/<username>/

    Method: GET

    View: start_chat

    Description: Initiates chat with another user


# RESTful API Endpoints (Return JSON)

## 1. Authentication Token
        URL: /api/token_auth/

        Method: POST

        View: CustomObtainAuthToken

        Description: Generates auth token
```
curl -X POST http://localhost/api/token_auth/ \
     -d '{"email":"user@example.com", "password":"yourpassword"}' \
     -H "Content-Type: application/json"
```



## 2. Full Chats History
        URL: /api/chat_history/

        Method: GET

        View: ChatHistoryAPIView

        Description: Retrieves chat history for all users, User must be a superUser

```
curl http://localhost/api/chat_history/ \
     -H "Authorization: Token <your_token>"
```

## 3. Full Chat History between 2 users

        URL: /api/chat_history/<username>

        METHOD: GET

        View: ChatHistoryByUserAPIView

        Description: Retrieve chat history between auth token {username}.

```
curl http://localhost/api/chat_history/<username>/ \
     -H "Authorization: Token <authToken>"
```
