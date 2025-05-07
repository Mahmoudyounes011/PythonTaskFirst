# Student Management API with Authentication

A secure RESTful API for managing student records and user authentication using Flask, MySQL, and JWT.

## Features
- ✅ User Authentication (Register/Login/Logout)
- 🔑 JWT Token-based Authorization
- 📧 Welcome Email Notification on Login
- 🗄️ Student CRUD Operations
- 🛡️ Token Revocation System
- 🚨 Comprehensive Error Handling
- 📊 MySQL Database Integration
- 🔄 Refresh Token Mechanism

## Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- Git
- Postman (for API testing)
- SMTP Email Service (mailTrap)

### Installation
```bash
git clone https://github.com/Mahmoudyounes011/PythonTaskFirst.git
cd student-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
