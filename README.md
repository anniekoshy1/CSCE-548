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
```bash
python create_db.py
```bash
python service.py

In a separate terminal window:
```bash
python client.py
