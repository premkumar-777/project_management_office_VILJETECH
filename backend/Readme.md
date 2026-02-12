**PMO Platform Backend - README**


Backend run command:
uvicorn app.main:app --reload

Frontend run command:
npm run dev

**Overview**
This backend is built using FastAPI and SQLAlchemy for a Project Management Office (PMO) platform.

It supports:
Role-Based Access Control (RBAC)
Multi-Factor Authentication (MFA)
User Management
Client Management
The backend exposes RESTful APIs for frontend applications (React, Angular, etc.).

**Architecture & Components**

1. FastAPI

Handles routing, request validation, and responses.
Provides automatic OpenAPI documentation at /docs.

2. Database
SQLAlchemy ORM is used for models and interactions.

Tables include:
users: Stores platform users (super-admin, admin, employees)
roles: Role definitions (super-admin, admin, user)
user_roles: Mapping users to roles
clients: Stores clients added by super-admin/admin
Database is configurable via app/database.py (MySQL, SQL Server, or PostgreSQL supported).

**Database Tables******

**Users Table**
| Column        | Type         | Description                      |
| ------------- | ------------ | -------------------------------- |
| id            | int          | Auto-increment primary key       |
| name          | varchar(100) | User full name                   |
| email         | varchar(150) | User email                       |
| password_hash | varchar(255) | Hashed password                  |
| status_id     | int          | Status of the user               |
| location      | varchar(100) | User location                    |
| created_by    | int          | ID of user who created this user |
| deleted_by    | int          | ID of user who deleted this user |
| created_at    | timestamp    | Creation timestamp               |
| updated_at    | timestamp    | Last update timestamp            |
| mfa_secret    | varchar(255) | MFA secret (for OTP)             |
| mfa_enabled   | tinyint(1)   | MFA enabled flag (0 or 1)        |


**Clients Table**
| Column      | Type         | Description                        |
| ----------- | ------------ | ---------------------------------- |
| id          | int          | Auto-increment primary key         |
| name        | varchar(100) | Client name                        |
| email       | varchar(150) | Client email                       |
| status_id   | int          | Status of the client               |
| location    | varchar(100) | Client location                    |
| created_by  | int          | ID of user who added this client   |
| deleted_by  | int          | ID of user who deleted this client |
| created_at  | timestamp    | Creation timestamp                 |
| updated_at  | timestamp    | Last update timestamp              |
| mfa_secret  | varchar(255) | Optional MFA secret                |
| mfa_enabled | tinyint(1)   | MFA enabled flag (0 or 1)          |

**Roles Table**
| Column      | Type         | Description                          |
| ----------- | ------------ | ------------------------------------ |
| id          | int          | Auto-increment primary key           |
| name        | varchar(50)  | Role name (super-admin, admin, user) |
| description | varchar(255) | Optional description                 |
| created_at  | timestamp    | Creation timestamp                   |
| updated_at  | timestamp    | Last update timestamp                |


**User Roles Mapping Table**
| Column      | Type      | Description                      |
| ----------- | --------- | -------------------------------- |
| id          | int       | Auto-increment primary key       |
| user_id     | int       | ID of the user                   |
| role_id     | int       | ID of the role                   |
| assigned_by | int       | ID of user who assigned the role |
| created_at  | timestamp | Assignment timestamp             |

**Authentication & API Endpoints******

Authentication:
| Endpoint           | Method | Description                              | Request Body                           | Response                                                      |
| ------------------ | ------ | ---------------------------------------- | -------------------------------------- | ------------------------------------------------------------- |
| /auth/login        | POST   | Login user with email & password         | `{ "email": "", "password": "" }`      | `{ "temp_token": "..." }`                                     |
| /auth/set-password | POST   | First-time password setup, generates MFA | `{ "temp_token": "", "password": "" }` | `{ "mfa_required": true, "qr_uri": "" }`                      |
| /auth/verify-mfa   | POST   | Verify MFA OTP                           | `{ "temp_token": "", "otp": "" }`      | `{ "access_token": "", "token_type": "bearer", "roles": [] }` |

Users:
| Endpoint   | Method | Description                       | Request Body                                                               | Notes                                                                            |
| ---------- | ------ | --------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| /users/add | POST   | Super-admin/Admin adds a new user | `{ "name": "", "email": "", "roles": [], "location": "", "status_id": 1 }` | Admin cannot create super-admin or admin users. Returns temp_token & invite URL. |

**Roles & Permissions**
| Role        | Can Add Users                | Can Add Clients | MFA Required |
| ----------- | ---------------------------- | --------------- | ------------ |
| Super-admin | ✅                            | ✅               | ✅            |
| Admin       | ✅ (except admin/super-admin) | ✅               | ✅            |
| User        | ❌                            | ❌               | Optional     |
| Client      | ❌                            | ❌               | Optional     |

MFA (Multi-Factor Authentication)

Enabled via pyotp

Users generate a QR code URI at first login

Columns added to users table:

ALTER TABLE users ADD COLUMN mfa_secret VARCHAR(255);
ALTER TABLE users ADD COLUMN mfa_enabled TINYINT DEFAULT 0;


Optional for clients:

ALTER TABLE clients ADD COLUMN mfa_secret VARCHAR(255);
ALTER TABLE clients ADD COLUMN mfa_enabled TINYINT DEFAULT 0;

Frontend Integration Guide

Login Flow:

Call /auth/login → get temp_token

Call /auth/set-password → get qr_uri for MFA

Call /auth/verify-mfa → get access_token

Authorization Header:

Authorization: Bearer <access_token>


User Management:

Use /users/add to add employees

Frontend should check current_user.role_names

Client Management:

Use /clients/add to add clients

MFA optional

Security Notes

Passwords hashed using bcrypt

JWT tokens signed with SECRET_KEY using HS256

MFA secrets stored in DB; never return raw secrets after initial QR URI

Running Locally
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

# Swagger docs
http://127.0.0.1:8000/docs


