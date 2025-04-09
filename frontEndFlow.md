# Q&A Web Application

A full-stack question-and-answer web platform that allows users to register, login, post questions, answer others' questions, and interact through likes/dislikes.

## Features

- **User Authentication**
  - Register via `/register` page.
  - Login via `/login` page.
  - JWT-based authentication.
  
- **Dashboard Functionalities**
  - View all questions from all users.
  - Post a new question.
  - View only your questions.
  - Archive your questions.
  - View answers for each question.
  - Post answers to any question.
  - Like/Dislike answers.
  - Logout from current or other devices.
  - Refresh questions list.

---

## Frontend

### Register

- **URL**: `http://localhost:5173/register`
- **Fields**: Username, Password
- **Action**: Creates a new user account.

### Login

- **URL**: `http://localhost:5173/login`
- **Request Payload**:
  ```json
  {
    "username": "nihar",
    "password": "nihar"
  }
  ```
- **Response**:
  ```json
  {
    "Status": "Success",
    "Message": "User Logged in",
    "accessToken": "<JWT_TOKEN>"
  }
  ```

- On successful login, redirects to Dashboard and fetches all questions from backend.

---

## Backend API Endpoints

### 1. Get All Questions

- **GET** `/api/get-all-questions`
- **Response**:
  ```json
  {
    "Status": "Success",
    "Message": "Questions retrieved successfully",
    "Data": [],
    "accessToken": "<JWT_TOKEN>"
  }
  ```

### 2. Post Question

- **POST** `/api/post-question`
- **Request**:
  ```json
  {
    "question": "What is the capital of Canada"
  }
  ```

- **Response**:
  ```json
  {
    "Status": "Success",
    "Message": "Question posted successfully",
    "questionId": 2,
    "accessToken": "<JWT_TOKEN>"
  }
  ```

### 3. Get My Questions

- **GET** `/api/get-my-questions`
- **Response**:
  ```json
  {
    "Status": "Success",
    "Message": "Your questions retrieved successfully",
    "Data": [
      {
        "id": 1,
        "question": "Example question?",
        "username": "nihar",
        "isActive": true
      }
    ],
    "accessToken": "<JWT_TOKEN>"
  }
  ```

### 4. Get Answers

- **POST** `/api/get-answer`
- **Request**:
  ```json
  {
    "questionId": 1
  }
  ```
- **Response**:
  ```json
  {
    "Status": "Success",
    "Message": "Answers retrieved successfully",
    "Data": [],
    "accessToken": "<JWT_TOKEN>"
  }
  ```

### 5. Archive Question

- **POST** `/api/archive-question`
- **Request**:
  ```json
  {
    "questionId": 1
  }
  ```
- **Response**:
  ```json
  {
    "Status": "Success",
    "Message": "Question archived successfully",
    "Data": {
      "questionId": 1,
      "isActive": false
    },
    "accessToken": "<JWT_TOKEN>"
  }
  ```

### 6. Post Answer

- **POST** `/api/post-answer`
- **Request**:
  ```json
  {
    "answer": "This is the answer",
    "questionId": 1
  }
  ```
- **Response**:
  ```json
  {
    "Status": "Success",
    "Message": "Answer posted successfully",
    "answerId": 1,
    "accessToken": "<JWT_TOKEN>"
  }
  ```

### 7. Like / Dislike Answer

- **POST** `/api/likes-dislikes`
- **Request** (Like):
  ```json
  {
    "answerId": 1,
    "like": "True",
    "dislike": "False"
  }
  ```
- **Request** (Dislike):
  ```json
  {
    "answerId": 1,
    "like": "False",
    "dislike": "True"
  }
  ```

- **Response**:
  ```json
  {
    "Status": "Success",
    "likes": 1,
    "dislikes": 0,
    "accessToken": "<JWT_TOKEN>"
  }
  ```

---

## Logout Options

- **Logout**
  - Deletes current refresh token.
  - Removes token from local storage.

- **Logout from other devices**
  - Removes all refresh and access tokens except the current one.

---

## Notes

- Every API returns a refreshed `accessToken` on success (except logout).
- Token should be included in the Authorization header as: `Bearer <accessToken>`.

---

## Tech Stack

- **Frontend**: React.js
- **Backend**: Django / FastAPI (assumed)
- **Authentication**: JWT
- **Storage**: LocalStorage (Frontend)

---

## Setup Instructions

1. Clone the repository.
2. Install frontend and backend dependencies.
3. Run backend server at `http://localhost:8000/`
4. Run frontend using:
   ```bash
   npm install
   npm run dev
   ```
5. Access the app at `http://localhost:5173`

---

## Author

Nihar
