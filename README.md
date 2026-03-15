# CSCE 548 Project 4 – Assignment Tracker

N tier web application

The system includes:

• Data Layer
• Business Layer
• Service Layer
• Client Layer

---

## Technologies Used

Python  
Flask  
SQLite  
React  
Vite  
JavaScript  

---

## How to Run the Project

### 1. Clone the Repository

git clone https://github.com/anniekoshy1/CSCE-548

cd CSCE-548

---

### 2. Install Python Dependencies

pip install flask flask-cors

---

### 3. Initialize the Database

python init_db.py

---

### 4. Start the Backend Service

python service.py

The API runs at:

http://127.0.0.1:5000

---

### 5. Start the Frontend Client

cd client

npm install

npm run dev

Open:

http://localhost:5173

---

## System Testing

System functionality was tested through the client interface and API.

The following operations were tested:

• Create user  
• Get all users  
• Get single user  
• Update user

Screenshots of these tests are included in:

project4deployment.pdf

---

## Author

Annie Koshy  
CSCE 548



# CSCE 548 – Project 2  
Assignment Tracker

This project includes:
- **Data Layer (`db.py`)** – Handles direct interaction with the SQLite database.
- **Business Layer (`business.py`)** – Wraps all data-layer CRUD operations and contains validation logic.
- **Service Layer (`service.py`)** – Exposes business-layer functionality through a Flask-based REST API.
- **Console Client (`client.py`)** – Invokes the service layer to demonstrate full CRUD functionality.

## Running the Project Locally

### 1. Install Dependencies

```bash
pip install -r requirements.txt
python create_db.py
python service.py

In a separate terminal window:
```bash
python client.py
