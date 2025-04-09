# TransportSimple-Assignment
This repository contains both frontend and backend components for the TransportSimple-Assignment project.

## Prerequisites
- **Python**: Ensure Python is installed on your system.
- **Virtualenv**: Install virtualenv using `pip install virtualenv`.
- **Node.js and npm**: Ensure Node.js and npm are installed for the frontend.

## Setup Instructions

### Clone the Repository
1. Clone the repository using the following command:
git clone https://github.com/niharMohantyDev/TransportSimple-Assignment.git

text

2. Open the cloned directory in a terminal.

### Frontend Setup
1. Navigate to the frontend directory:
cd .\TransportSimple-Assignment\Client\

text

2. Install dependencies:
npm i

text

3. Start the frontend server:
npm run dev

text

### Backend Setup
1. Navigate to the backend directory:
cd .\TransportSimple-Assignment\Server\

text

2. Create a virtual environment:
virtualenv venv

text

3. Activate the virtual environment:
- If your execution policy is restricted, you may need to adjust it first:
  ```
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
  .\venv\Scripts\activate.ps1 -ExecutionPolicy Bypass
  ```
- Otherwise, use:
  ```
  .\venv\Scripts\activate
  ```

4. Install backend dependencies:
pip install -r requirements.txt

text

5. Start the backend server:
py manage.py runserver 8000

text

## Running the Application
- Ensure both frontend and backend servers are running.
- Access the application through the frontend URL provided by `npm run dev`.

## Troubleshooting
- If you encounter issues with virtual environment activation, check your system's execution policy settings.
- Ensure all dependencies are correctly installed before running the servers.
