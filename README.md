# Invoicing API

A Django REST Framework API for small business invoicing with customers, invoices, and line items.

## Features

- Create and manage customers
- Create invoices with multiple line items
- Automatic total calculations
- Invoice status tracking (pending/paid/overdue)
- RESTful API endpoints

## Prerequisites

- Python 3.8+
- PostgreSQL (recommended) or SQLite
- pip

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/invoicing-api.git
cd invoicing-api 
```

## Create and activate a virtual environment
python -m venv venv or virtualenv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

## Install dependencies
pip install -r requirements.txt

## Run Migrations
python manage.py migrate

## Running the Application
python manage.py runserver