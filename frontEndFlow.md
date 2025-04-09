# Quetion And Answers app

## Process to follow

### Step 1

#### enter the url http://localhost:5173/register
#### enter username and password and register

### Step 2

#### enter the url http://localhost:5173/login

#### for login enter username and password n api request will be like

```json
{
    "username": "nihar",
    "password": "nihar"
}
```

#### and response will be like

```json
{
    "Status": "Success",
    "Message": "User Logged in",
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MTk0MTg0LCJpYXQiOjE3NDQxOTM4ODQsImp0aSI6IjhlMzYwYzIyZTE3YjQxOWZiYThlZjNjNmE2NGZjNjA5IiwidXNlcl9pZCI6MX0.PhwAE8W192BLtCmLxlb1eaq3NAthmGwlgsK4pRcDMEY"
}
```

### Step 3

#### After login you will see the dashboard which will hit the get endpoint "http://localhost:8000/api/get-all-questions" which will give me the response like

```json
{
    "Status": "Success",
    "Message": "Questions retrieved successfully",
    "Data": [],
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MTk0MTg0LCJpYXQiOjE3NDQxOTM4ODQsImp0aSI6IjhlMzYwYzIyZTE3YjQxOWZiYThlZjNjNmE2NGZjNjA5IiwidXNlcl9pZCI6MX0.PhwAE8W192BLtCmLxlb1eaq3NAthmGwlgsK4pRcDMEY"
}
```


#### The "Data" array will have list of questions as objects


### Step 4

#### Now in the Dashboard you can see 5 buttons

+ Logout:
##### This button will logout you and delete the refresh token and also delete the token from local storage
***
+ Logout from other devices:
##### this button will logout you from all other browser if you are logged in by deleting the refresh tokens and associated access tokens except the current access token from which you are logged in.

***
+ Add New Question:
##### when you click this button a prompt will open where you can input your question. on hitting Ok button this will call the endpoint "http://localhost:8000/api/post-question" with request simillar to
```json
{question: "What is the capital of Canada"}
```
##### and response you will get similar to
```json
{
    "Status": "Success",
    "Message": "Question posted successfully",
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MTk0NzQ1LCJpYXQiOjE3NDQxOTM4ODQsImp0aSI6ImIzMjRmMzU4YWEzMTQ3N2E5ZDBlMDNjOTRlMTgwYTYyIiwidXNlcl9pZCI6MX0.saKVpiFIP2tfqvAYw-TosGtIXeito8oORYdK0_U1RBk",
    "questionId": 2
}
```
##### after this it will it will again hit "http://localhost:8000/api/get-all-questions" for rerender and the response from backend will be like

```json
{
    "Status": "Success",
    "Message": "Questions retrieved successfully",
    "Data": [// Some list of question(s)],
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MTk0MTg0LCJpYXQiOjE3NDQxOTM4ODQsImp0aSI6IjhlMzYwYzIyZTE3YjQxOWZiYThlZjNjNmE2NGZjNjA5IiwidXNlcl9pZCI6MX0.PhwAE8W192BLtCmLxlb1eaq3NAthmGwlgsK4pRcDMEY"
}
```
***
+ Questions I Asked:
##### This button will hit "http://127.0.0.1:8000/api/get-my-questions" which is basically questions which are posted by you and its response will be like

```json
{
    "Status": "Success",
    "Message": "Your questions retrieved successfully",
    "Data": [
        {
            "id": 1,
            "question": "dvsdvfdvvdf",
            "username": "nihar",
            "isActive": true
        },
        {
            "id": 2,
            "question": "vfvbfdb",
            "username": "nihar",
            "isActive": true
        }
    ],
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MTk1MjQ0LCJpYXQiOjE3NDQxOTQ5NDQsImp0aSI6IjQ3ZjZjYTViNmNlNzRkOGM4YzFhMzRhYTY0ZjBiOWFlIiwidXNlcl9pZCI6MX0.Sxdav_xfLOKUzxWQDAw-wWoPTiDkpZGjy1VK7Ux8zpo"

}
```

##### the questions will be rendered as each card per each question.

when you will click the card it will hit "http://localhost:8000/api/get-answer"
with request 

```json
{questionId: 1}
```

##### and response as 
```json
{
    "Status": "Success",
    "Message": "Answers retrieved successfully",
    "Data": [],
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MTk1MjQ0LCJpYXQiOjE3NDQxOTQ5NDQsImp0aSI6IjQ3ZjZjYTViNmNlNzRkOGM4YzFhMzRhYTY0ZjBiOWFlIiwidXNlcl9pZCI6MX0.Sxdav_xfLOKUzxWQDAw-wWoPTiDkpZGjy1VK7Ux8zpo"
}
```

##### so the answers will have all the details, like answer and like and dislike counts.

on the question card there is also a button named as "Archive" which on click will hit "http://localhost:8000/api/archive-question"
with request similar to
```json
{
    "Status": "Success",
    "Message": "Question archived successfully",
    "Data": {
        "questionId": 1,
        "isActive": false
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MTk1MjQ0LCJpYXQiOjE3NDQxOTQ5NDQsImp0aSI6IjQ3ZjZjYTViNmNlNzRkOGM4YzFhMzRhYTY0ZjBiOWFlIiwidXNlcl9pZCI6MX0.Sxdav_xfLOKUzxWQDAw-wWoPTiDkpZGjy1VK7Ux8zpo"
}

```
##### this will basically archive your answer and not be visible on the UI.
***
+ Refresh Questions:
##### this button will hit a get request "http://localhost:8000/api/get-all-questions" and it will return 

```json
{
    "Status": "Success",
    "Message": "Questions retrieved successfully",
    "Data": [],
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MTk1NTk0LCJpYXQiOjE3NDQxOTQ5NDQsImp0aSI6IjVlYmJiNjIyMDkyOTRhMzI5NDgwOWU2ZDJhMDRmMWE1IiwidXNlcl9pZCI6MX0.ZsKLACdgkLVasZsVPDGgnt6dm7PZ3MZSNSnOcTmq70M"
}

```
***

### Step 5

#### you can also see a heading "Questions from everybody"

this will render all the questions posted by everybody else. the api was hit just after successful login - (mention above in login section)

while clicking on the question you will be provided with a text box which onSubmit will hit "http://localhost:8000/api/post-answer"
with request 

```bash
{
    "answer":"cdscs",
    "questionId": 1
}
```

#### and response will be similar to

```bash
{
    "Status": "Success",
    "Message": "Answer posted successfully",
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MTk2MTAxLCJpYXQiOjE3NDQxOTU4MDEsImp0aSI6ImIxNjFiZTRmYjg2NTRhOGNiMTBhMDk1MzliM2Y2ZDRiIiwidXNlcl9pZCI6Mn0.7ptlC1GVRmaimF1lBKAMYLElNrp2oBAcv53W5GBnJ0A",
    "answerId": 1
}
```

#### on your answer there is a like and dislike button, which you can like and also other users can like.

the like and dislike button will hit the api "http://localhost:8000/api/likes-dislikes"

with request

```bash
{answerId: 1, like: "True", dislike: "False"} //if you like the answer
{answerId: 1, like: "False", dislike: "True"} //if you dsilike the answer
```

#### and the response for that will be silillar to

```bash
{
    "Status": "Success",
    "likes": 1,
    "dislikes": 0,
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MTk2MTAxLCJpYXQiOjE3NDQxOTU4MDEsImp0aSI6ImIxNjFiZTRmYjg2NTRhOGNiMTBhMDk1MzliM2Y2ZDRiIiwidXNlcl9pZCI6Mn0.7ptlC1GVRmaimF1lBKAMYLElNrp2oBAcv53W5GBnJ0A"
}
```

---
## Important Note:
### As you might see i am returning access token on every api call except logout .
the reason for that is that access token is getting refreshed every 5 minutes, and so in localstorage i am updating the refreshed access token.
