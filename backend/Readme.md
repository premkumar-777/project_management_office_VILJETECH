PMO Platform Backend - README
Overview

This backend is built using FastAPI and SQLAlchemy for a Project Management Office (PMO) platform.
It supports role-based access control, multi-factor authentication (MFA), user management, and client management.

The backend exposes RESTful APIs that can be consumed by frontend applications (React, Angular, etc.).
______________________________
Backend run command:
uvicorn app.main:app --reload

Frontend run command:
npm run dev

_______________________________


Architecture & Components
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

3. Authentication & Authorization

JWT-based authentication.

Endpoints:

Authentication
Endpoint	Method	Description	Request Body	Response
/auth/login	POST	Login user with email & password	{ "email": "", "password": "" }	{ "temp_token": "..." }
/auth/set-password	POST	First-time password setup, generates MFA	{ "temp_token": "", "password": "" }	{ "mfa_required": true, "qr_uri": "" }
/auth/verify-mfa	POST	Verify MFA OTP	{ "temp_token": "", "otp": "" }	{ "access_token": "", "token_type": "bearer", "roles": [] }