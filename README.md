# ==============================================================================
# CLIENT QUERY MANAGEMENT SYSTEM (CQMS)
# ==============================================================================
#
# A Streamlit-based web application for managing client support queries with
# secure authentication, ticket tracking, analytics dashboard, and support
# team operations using PostgreSQL.
#
# ==============================================================================

## Project Overview

The **Client Query Management System (CQMS)** is a role-based support ticket application developed using **Python, Streamlit, and PostgreSQL**.

This project allows:

- **Clients** to raise support queries
- **Support team** to manage and resolve tickets
- **Secure login system** with password hashing
- **Dashboard analytics** for monitoring tickets

This is a real-world support workflow project suitable for:
- Python Developer portfolio
- QA / Testing portfolio
- Data dashboard projects
- SQL + Python integration showcase

---

## Features

### Client Portal
- Secure login authentication
- Submit new support queries
- Track query history
- View query status
- Password reset
- Query metrics dashboard

### Support Dashboard
- Register new users
- View all client queries
- Filter by phone number
- Filter by status
- Close active tickets
- Dashboard statistics
- Visual charts

### Analytics
- Open vs Closed query distribution
- Query category count
- Support performance monitoring

---

## Tech Stack

| Technology | Purpose |
|-----------|----------|
| Python | Core programming |
| Streamlit | Frontend UI |
| PostgreSQL | Database |
| Pandas | Data processing |
| Matplotlib | Charts |
| bcrypt | Password hashing |
| psycopg2 | DB connection |

---

## Project Structure

```bash
CQMS/
│
├── main.py            # Application entry point
├── client.py          # Client dashboard
├── support.py         # Support dashboard
├── db_code.py         # Database operations
├── requirements.txt   # Dependencies
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/client-query-management-system.git
cd client-query-management-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

### Windows
```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database Setup

Create PostgreSQL database:

```sql
CREATE DATABASE Client_QueryDB;
```

Update credentials inside `db_code.py`

```python
conn = psycopg2.connect(
    host="localhost",
    database="Client_QueryDB",
    user="postgres",
    password="your_password"
)
```

Required SQL functions / procedures:

- `insert_user_fn()`
- `insert_query()`
- `get_all_queries()`
- `close_query()`
- `update_password_secure()`

---

## Run Application

```bash
streamlit run main.py
```

---

## Screens Included

- Login Page
- Client Portal
- Support Dashboard
- Ticket Reports
- Query Analytics

---

## Security Features

- Password hashing using bcrypt
- Role-based authentication
- Secure password reset
- SQL function-based DB operations

---

## Future Enhancements

- Email notifications
- Ticket priority
- Export to Excel / PDF
- Admin panel
- Deployment on Streamlit Cloud

---

## Author

**Developed by Vinodhini**

GitHub Portfolio Project — Python + SQL + Streamlit
