**PMO Platform **
Overview

This backend is built using FastAPI and SQLAlchemy for a Project Management Office (PMO) platform.
It supports role-based access control, multi-factor authentication (MFA), user management, and client management.

The backend exposes RESTful APIs that can be consumed by frontend applications (React, Angular, etc.).

Backend run command:

uvicorn app.main:app --reload


Frontend run command:

npm run dev

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
Users
Endpoint	Method	Description	Request Body	Notes
/users/add	POST	Super-admin/Admin adds a new user	{ "name": "", "email": "", "roles": [], "location": "", "status_id": 1 }	Admin cannot create super-admin or admin users. Returns temp_token & invite URL.
Clients
Endpoint	Method	Description	Request Body	Notes
/clients/add	POST	Super-admin/Admin adds a new client	{ "name": "", "email": "", "status_id": 1 }	Stored in clients table. Can include optional mfa_enabled & mfa_secret.
Roles & Permissions
Role	Can Add Users	Can Add Clients	MFA Required
Super-admin	✅	✅	✅
Admin	✅ (except admin/super-admin)	✅	✅
User	❌	❌	Optional
Client	❌	❌	Optional

Roles are checked in the get_current_user dependency, available in current_user.role_names.

MFA (Multi-Factor Authentication)

Enabled via pyotp.

Users generate a QR code URI at first login.

MFA columns in users table:

ALTER TABLE users ADD COLUMN mfa_secret VARCHAR(255);
ALTER TABLE users ADD COLUMN mfa_enabled TINYINT DEFAULT 0;


MFA optional for clients:

ALTER TABLE clients ADD COLUMN mfa_secret VARCHAR(255);
ALTER TABLE clients ADD COLUMN mfa_enabled TINYINT DEFAULT 0;

Frontend Integration Guide
Login Flow

Call /auth/login → get temp_token.

Call /auth/set-password for first-time login → get qr_uri for MFA.

Call /auth/verify-mfa → get access_token for future requests.

Authorization

Include JWT token in header:

Authorization: Bearer <access_token>

User Management

Use /users/add to add employees.

Frontend should check current_user.role_names before displaying restricted actions.

Client Management

Use /clients/add to add clients.

Can optionally implement MFA for clients.

Database Notes

users table contains fields for MFA, status, roles mapping.

clients table mirrors users table (except password hashing; MFA optional).

All IDs are auto-incremented.

Roles are mapped via user_roles table.

Security Notes

Passwords hashed using bcrypt.

JWT tokens signed using SECRET_KEY with HS256 algorithm.

MFA secrets stored in DB; never return raw secrets to frontend after initial QR URI.

Running Locally
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

# Swagger docs available at
http://127.0.0.1:8000/docs

Notes for Frontend Developers

Always use the access_token in Authorization headers for all protected endpoints.

Check current_user.role_names for rendering role-specific UI.

Use invite_url from /users/add to trigger first-time password setup.

Super-admin can access all endpoints; admins are restricted by role rules.

Clients are now stored in their own table (optional MFA supported).
