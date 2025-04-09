# TransportSimple Assignment

This project consists of a Frontend (React) and Backend (Django) setup for the TransportSimple Assignment.

---

## Getting Started

Follow the steps below to run the application on your local system.

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/niharMohantyDev/TransportSimple-Assignment.git
```

---

## Step 2: Frontend Setup

1. Navigate to the client directory:

```bash
cd .\TransportSimple-Assignment\Client\
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

---

## Step 3: Backend Setup

1. Navigate to the server directory:

```bash
cd .\TransportSimple-Assignment\Server\
```

2. Create a virtual environment (make sure Python and `virtualenv` are installed):

```bash
virtualenv venv
```

> To install `virtualenv` if not already installed:

```bash
pip install virtualenv
```

3. Activate the virtual environment:

```bash
.\venv\Scripts\activate
```

> **Note:** If you get a policy restriction error, run:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\activate.ps1 -ExecutionPolicy Bypass
```

4. Install project dependencies:

```bash
pip install -r requirements.txt
```

5. Run the Django development server:

```bash
py manage.py runserver 8000
```

---

## Notes

- Make sure Python is installed on your system.
- The frontend runs on Vite + React.
- The backend is built with Django and requires the virtual environment for isolated dependencies.

---

Happy Coding!
