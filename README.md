TransportSimple Assignment
This project consists of a Frontend (React) and Backend (Django) setup for the TransportSimple Assignment.

Getting Started
Follow the steps below to run the application on your local system.

Step 1: Clone the Repository
git clone https://github.com/niharMohantyDev/TransportSimple-Assignment.git
Step 2: Frontend Setup
Navigate to the client directory:
cd .\TransportSimple-Assignment\Client\
Install dependencies:
npm install
Start the development server:
npm run dev
Step 3: Backend Setup
Navigate to the server directory:
cd .\TransportSimple-Assignment\Server\
Create a virtual environment (make sure Python and virtualenv are installed):
virtualenv venv
To install virtualenv if not already installed:

pip install virtualenv
Activate the virtual environment:
.\venv\Scripts\activate
Note: If you get a policy restriction error, run:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\activate.ps1 -ExecutionPolicy Bypass
Install project dependencies:
pip install -r requirements.txt
Run the Django development server:
py manage.py runserver 8000
Notes
Make sure Python is installed on your system.
The frontend runs on Vite + React.
The backend is built with Django and requires the virtual environment for isolated dependencies.
