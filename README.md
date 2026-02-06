# MediSure Backend API

Django REST API for the MediSure medicine track-and-trace system on Cardano.

## Live Deployment

**Backend API:** https://medisure-backend-t5yr.onrender.com/api/

## Local Setup

1. Create virtual environment and activate it:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file in backend folder:
```
BLOCKFROST_PROJECT_ID=your_testnet_api_key_here
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Start server:
```bash
python manage.py runserver
```

## API Endpoints

**Live Base URL:** `https://medisure-backend-t5yr.onrender.com/api/`
**Local Base URL:** `http://127.0.0.1:8000/api/`

### Authentication

**POST /api/auth/signup/**
```json
{
  "username": "user123",
  "password": "password",
  "email": "user@example.com",
  "role": "patient"
}
```

**POST /api/auth/signin/**
```json
{
  "username": "user123",
  "password": "password"
}
```

### Blockchain Endpoints

**POST /api/mint/**
- Mint a new batch NFT

**POST /api/transfer/**
- Transfer batch between supply chain entities

**GET /api/verify/{qr_code}/**
- Verify medicine authenticity via QR code

**GET /api/journey/{batch_id}/**
- Track batch journey through supply chain

### Dashboard

**GET /api/dashboard/?manufacturer_id={uuid}**
- Get manufacturer dashboard statistics

### Pharmacy Inventory

**GET /api/inventory/**
- List all pharmacy inventory

**POST /api/inventory/**
- Add medicine to pharmacy inventory

**GET /api/pharmacy/{pharmacy_id}/inventory/**
- Get inventory for specific pharmacy

### Shopping Cart

**GET /api/cart/?user_id={id}**
- Get user's cart

**POST /api/cart/add/**
```json
{
  "user_id": 1,
  "inventory_id": "uuid",
  "quantity": 2
}
```

**PUT /api/cart/update/{item_id}/**
- Update cart item quantity

**DELETE /api/cart/remove/{item_id}/**
- Remove item from cart

**DELETE /api/cart/clear/?user_id={id}**
- Clear entire cart

### Orders

**POST /api/orders/create/**
```json
{
  "user_id": 1,
  "pharmacy_id": "uuid"
}
```

**GET /api/orders/?user_id={id}**
- Get user's order history

**GET /api/orders/{order_id}/**
- Get specific order details

**PUT /api/orders/{order_id}/status/**
```json
{
  "status": "confirmed"
}
```

### Users

**GET /api/users/{user_id}/**
- Get user details

**GET /api/users/?role={role}**
- List users by role (manufacturer, distributor, pharmacy, patient)

### CRUD Endpoints

- `/api/manufacturers/` - Manage manufacturers
- `/api/distributors/` - Manage distributors
- `/api/pharmacies/` - Manage pharmacies
- `/api/batches/` - Manage batches
- `/api/transactions/` - View transactions

## Technologies

- Django 5.2
- Django REST Framework
- Blockfrost API (Cardano)
- SQLite (development) / PostgreSQL (production)
- Python 3.11+