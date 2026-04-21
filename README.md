# Marketplace Management System

A CLI-based marketplace management application supporting three user roles: Admin, Merchant, and Client. Admins configure and manage markets on a 2D spatial grid, assigning positions to merchants. Merchants manage their product inventory and pricing. Clients browse available products, place orders, and track their transaction history. Authentication is secured with bcrypt, all data is persisted in MongoDB, and the terminal interface is rendered with the Rich library. A Plotly/Dash web dashboard provides administrators with real-time sales visualization and analytics.

## Features

- Multi-role access control: Admin, Merchant, and Client workflows
- 2D grid-based market positioning system managed by administrators
- MongoDB-backed data persistence for users, products, and transactions
- Rich terminal UI for an improved CLI experience
- Plotly/Dash dashboard for sales and inventory visualization
- bcrypt password hashing for secure authentication
- Transaction history tracking per client

## Tech Stack

- Python 3
- MongoDB (via PyMongo)
- Rich (terminal UI)
- Plotly / Dash (visualization dashboard)
- bcrypt (authentication)
- Docker Compose (MongoDB service)

## Setup

1. Start the MongoDB service:
   ```bash
   docker compose up -d
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Project Structure

```
Core/           # Settings and utility functions
Database/       # MongoDB models and service layer
Market/         # Market management logic and views
Users/          # User management (admin, merchant, client)
Transactions/   # Order and transaction handling
Notifications/  # Notification services
Visualization/  # Dash/Plotly dashboard
docs/           # Project documentation and use cases
```
