# Secure Authentication System with 2FA and OAuth2
### Flask-Based Authentication System with TOTP and OAuth2 Authorization Code Flow

A secure authentication web application built using **Flask**, featuring:

1. **Two-Factor Authentication (2FA)** using TOTP (Google Authenticator).
2. **OAuth2 Authorization Code Flow** integration.
3. **Brute-force protection** and **bcrypt-hashed** passwords.
4. **SQLite database** for secure user data management.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation Guide](#installation-guide)
  - [Clone the Repository](#clone-the-repository)
  - [Create Virtual Environment](#create-virtual-environment)
  - [Install Dependencies](#install-dependencies)
  - [Environment Configuration](#environment-configuration)
  - [Initialize Database](#initialize-database)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
  - [Password Requirements](#password-requirements)  
  - [User Registration](#user-registration)
  - [User Login](#user-login)
  - [Enabling 2FA](#enabling-2fa)
  - [Logging in with 2FA](#logging-in-with-2fa)
  - [Disabling 2FA](#disabling-2fa)
  - [Set Up OAuth2](#set-up-oauth2)
- [Security Features](#security-features)
- [Database Schema](#database-schema)
- [Future Improvements](#future-improvements)

---

## Project Overview

This project implements a **secure authentication system** using **Flask**.  
It focuses on modern authentication principles, including strong password management, rate-limiting, and 2FA for enhanced account protection.  
The application also integrates **OAuth2 Authorization Code Flow** for third-party login support.

---

## Features

- **Database Integration:** SQLite database with secure schema design.  
- **Basic Authentication:** Username/password with bcrypt hashing.  
- **Brute Force Protection:** Account lockout after repeated failed attempts.  
- **Two-Factor Authentication (2FA):** TOTP with Google Authenticator.  
- **OAuth2 Integration:** Full Authorization Code Flow implementation.  

---

## Project Structure
```
.
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── routes/
│   │   ├── main.py
│   │   ├── password_auth.py
│   │   ├── two_factor.py
│   │   └── oauth.py
│   ├── services/
│   │   ├── db_helper.py
│   │   ├── hashing.py
│   │   └── timeout.py
│   ├── static/
│   │   └── css/
│   │       └── main.css
│   └── templates/
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── enable_2fa.html
│       └── verify_2fa.html
├── instance/
│   └── database.db
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## Installation Guide

### Clone the Repository
    ```bash
    git clone git@github.com:TobiasVeda/ikt222_assignment_3.git
    ```
    
    ```bash
    cd ikt222_assignment_3
    ```
### Create Virtual Environment
    ```bash
    python -m venv venv
    source venv/bin/activate      # Linux / macOS
    venv\Scripts\activate         # Windows
    ```
  
### Install Dependencies
    ```bash
    pip install -r requirements.txt 
  ```
## Running the Application
  ```bash
  python run.py
  ```
- Open your browser at:
  http://localhost:5000

## Usage Guide
### Password requirements:
1. At least 8 characters.
2. Uppercase and lowercase letters.
3. At least one number.
4. At least one special character.

### User Registration
1. Click Register
2. Enter Credentials
3. Click Register

### User Login
1. Click Login.
2. Enter your credentials.
3. If 2FA is enabled, you’ll be asked for your 6-digit code.

### Enabling 2FA
1. Log in and go to the dashboard.
2. Click Enable 2FA.
3. Scan the QR code using e.g. Google Authenticator.
4. Enter the displayed 6-digit code.
5. 2FA setup complete — store your secret key securely.

### Logging in with 2FA
1. Enter username and password.
2. Enter your 6-digit TOTP from Google Authenticator.
3. You’ll be redirected to your dashboard.

### Disabling 2FA
1. Go to the dashboard.
2. Click Disable 2FA.
3. Confirm the action.

### Set Up OAuth2
1. Login
2. Click OAuth2
3. Click what account you wish to utilise for OAuth2.

## Security Features
1. Password Hashing: bcrypt with automatic salting.
2. Account Lockout: After 3 failed attempts (progressive timeout).
3. 2FA (TOTP): 30-second rotating codes with ±30s tolerance.
4. Encrypted Secret Storage: All TOTP secrets stored securely in the database.
5. Session Security:
  1. HTTP-only cookies
  2. Optional HTTPS-only flag
  3. Session timeout (30 minutes)
  4. Built-in CSRF protection

## Database Schema
  ```bash
  CREATE TABLE users (
    id TEXT PRIMARY KEY NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    failed_attempts INTEGER DEFAULT 0,
    last_lockout TEXT DEFAULT NULL,
    lockout_streak INTEGER DEFAULT 0,
    totp_secret TEXT,
    two_factor_enabled INTEGER DEFAULT 0
    );
```

## Future Improvements
1. Add logout.
2. Add email verification on registration.
3. Password reset functionality.
4. Support for SMS/email-based 2FA.
