TransportSimple Assignment - Setup Guide
This guide will help you set up and run both the frontend and backend parts of the TransportSimple assignment project.

Prerequisites
Node.js installed (for frontend)

Python installed (for backend)

Git installed

Virtualenv installed (can be installed with pip install virtualenv)

Setup Instructions
1. Clone the Repository
bash
Copy
git clone https://github.com/niharMohantyDev/TransportSimple-Assignment.git
2. Navigate to the Project Directory
Right-click on the project folder and select "Open with Terminal" or open a terminal and navigate to the project directory manually.

Frontend Setup
Navigate to the Client directory:

bash
Copy
cd .\TransportSimple-Assignment\Client\
Install dependencies:

bash
Copy
npm i
Start the development server:

bash
Copy
npm run dev
Backend Setup
Navigate to the Server directory:

bash
Copy
cd .\TransportSimple-Assignment\Server\
Create a virtual environment:

bash
Copy
virtualenv venv
Activate the virtual environment:

bash
Copy
.\venv\Scripts\activate
If you encounter execution policy restrictions, run these commands first:

bash
Copy
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\activate.ps1 -ExecutionPolicy Bypass
Install backend dependencies:

bash
Copy
pip install -r requirements.txt
Start the backend server:

bash
Copy
py manage.py runserver 8000
Accessing the Application
Frontend will typically run on http://localhost:3000 (or the port specified in your frontend configuration)

Backend will run on http://localhost:8000
