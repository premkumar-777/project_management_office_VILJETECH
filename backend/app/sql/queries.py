# app/sql/queries.py

# ---------------- Users ----------------
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    status_id INT,
    location VARCHAR(100),
    created_by INT,
    deleted_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    mfa_secret VARCHAR(255),
    mfa_enabled TINYINT(1) DEFAULT 0,
    CONSTRAINT fk_users_status FOREIGN KEY (status_id) REFERENCES user_status(id) ON UPDATE CASCADE ON DELETE RESTRICT
);
"""

# ---------------- User Status ----------------
CREATE_USER_STATUS_TABLE = """
CREATE TABLE IF NOT EXISTS user_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(50) NOT NULL
);
"""

INSERT_USER_STATUS = """
INSERT INTO user_status (status) VALUES
('pending'),
('active'),
('hold');
"""

# ---------------- Roles ----------------
CREATE_ROLES_TABLE = """
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# ---------------- User Roles ----------------
CREATE_USER_ROLE_TABLE = """
CREATE TABLE IF NOT EXISTS user_roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);
"""

# ---------------- Clients ----------------
CREATE_CLIENTS_TABLE = """
CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    password_hash VARCHAR(255),
    status_id INT,
    created_by INT,
    deleted_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_clients_status FOREIGN KEY (status_id) REFERENCES user_status(id) ON UPDATE CASCADE ON DELETE RESTRICT
);
"""
# ________________________________________________

# ------------------------------
# Users Table Queries
# ------------------------------

# Fetch internal user by email
GET_USER_BY_EMAIL = """
SELECT *
FROM users
WHERE email = :email
"""

# Fetch internal user by ID
GET_USER_BY_ID = """
SELECT *
FROM users
WHERE id = :id
"""

# Insert new user
INSERT_USER = """
INSERT INTO users
(name, email, password_hash, status_id, location, created_by, created_at, updated_at, mfa_secret, mfa_enabled)
VALUES
(:name, :email, :password_hash, :status_id, :location, :created_by, NOW(), NOW(), :mfa_secret, :mfa_enabled)
"""

# Update user password
UPDATE_USER_PASSWORD = """
UPDATE users
SET password_hash = :password_hash, updated_at = NOW()
WHERE id = :user_id
"""

# Update user MFA secret and enable MFA
UPDATE_USER_MFA = """
UPDATE users
SET mfa_secret = :mfa_secret, mfa_enabled = :mfa_enabled, updated_at = NOW()
WHERE id = :user_id
"""

# ------------------------------
# User Roles Queries
# ------------------------------

# Get all roles for a user
GET_USER_ROLES = """
SELECT r.role
FROM roles r
JOIN user_roles ur ON r.id = ur.role_id
WHERE ur.user_id = :user_id
"""

# Insert user role
INSERT_USER_ROLE = """
INSERT INTO user_roles (user_id, role_id)
VALUES (:user_id, :role_id)
"""

# ------------------------------
# Roles Table Queries
# ------------------------------

# Get role by name
GET_ROLE_BY_NAME = """
SELECT *
FROM roles
WHERE role = :role
"""

# Get role by ID
GET_ROLE_BY_ID = """
SELECT *
FROM roles
WHERE id = :id
"""

# ------------------------------
# Clients Table Queries
# ------------------------------

# Fetch client by email
GET_CLIENT_BY_EMAIL = """
SELECT *
FROM clients
WHERE email = :email
"""

# Insert new client
INSERT_CLIENT = """
INSERT INTO clients
(name, email, password_hash, status_id, created_by, created_at, updated_at)
VALUES
(:name, :email, :password_hash, :status_id, :created_by, NOW(), NOW())
"""

# ------------------------------
# User Status Table Queries
# ------------------------------

# Fetch status by ID
GET_STATUS_BY_ID = """
SELECT *
FROM user_status
WHERE id = :id
"""

# Fetch status by name
GET_STATUS_BY_NAME = """
SELECT *
FROM user_status
WHERE status = :status
"""
# ________________________________________
# Insert a new user
INSERT_USER = """
INSERT INTO users (name, email, password_hash, status_id, location, created_by, created_at, mfa_secret, mfa_enabled)
VALUES (:name, :email, :password_hash, :status_id, :location, :created_by, NOW(), :mfa_secret, :mfa_enabled)
"""

# Assign roles to a user
ASSIGN_USER_ROLES = """
INSERT INTO user_roles (user_id, role_id)
VALUES (:user_id, :role_id)
"""

# Fetch roles of a user
GET_USER_ROLES = """
SELECT role_id FROM user_roles WHERE user_id = :user_id
"""
# _______________________________________________________

# app/sql/queries.py

# -------- USERS --------
CREATE_USER = """
INSERT INTO users 
(name, email, password_hash, status_id, location, created_by, mfa_secret, mfa_enabled)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

GET_USER_BY_EMAIL = "SELECT * FROM users WHERE email = %s"

GET_USER_BY_ID = "SELECT * FROM users WHERE id = %s"

# -------- CLIENTS --------
CREATE_CLIENT = """
INSERT INTO clients 
(name, email, password_hash, status_id, created_by)
VALUES (%s, %s, %s, %s, %s)
"""

GET_CLIENT_BY_EMAIL = "SELECT * FROM clients WHERE email = %s"

# -------- ROLES --------
GET_ROLE_BY_ID = "SELECT * FROM roles WHERE id = %s"
GET_ROLE_BY_NAME = "SELECT * FROM roles WHERE role = %s"

# -------- USER_ROLES --------
ASSIGN_ROLE = """
INSERT INTO user_roles
(user_id, role_id, assigned_by)
VALUES (%s, %s, %s)
"""

GET_USER_ROLES = "SELECT role_id FROM user_roles WHERE user_id = %s"

# -------- USER STATUS --------
GET_STATUS_BY_ID = "SELECT status FROM user_status WHERE id = %s"
GET_STATUS_BY_NAME = "SELECT id FROM user_status WHERE status = %s"


# ____________________________________________
# app/sql/queries.py

# Users
CREATE_USER = """
INSERT INTO users (name, email, password_hash, status_id, location, created_by, deleted_by, mfa_secret, mfa_enabled)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
GET_USER_BY_ID = "SELECT * FROM users WHERE id = %s"
GET_USER_BY_EMAIL = "SELECT * FROM users WHERE email = %s"

# Roles
GET_ROLE_BY_ID = "SELECT * FROM roles WHERE id = %s"
GET_ROLE_BY_NAME = "SELECT * FROM roles WHERE role = %s"

# User Roles
ASSIGN_ROLE = "INSERT INTO user_roles (user_id, role_id, assigned_by, created_at) VALUES (%s, %s, %s, NOW())"
GET_USER_ROLES = "SELECT role_id FROM user_roles WHERE user_id = %s"

# Clients
CREATE_CLIENT = """
INSERT INTO clients (name, email, password_hash, status_id, created_by, deleted_by, created_at, updated_at)
VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
"""
GET_CLIENT_BY_EMAIL = "SELECT * FROM clients WHERE email = %s"

# User Status
GET_STATUS_BY_ID = "SELECT * FROM user_status WHERE id = %s"
GET_STATUS_BY_NAME = "SELECT * FROM user_status WHERE status = %s"

# Users
GET_USER_BY_EMAIL = """
SELECT * FROM users WHERE email = :email
"""

GET_USER_BY_ID = """
SELECT * FROM users WHERE id = :user_id
"""

GET_USER_ROLES = """
SELECT r.role
FROM roles r
JOIN user_roles ur ON r.id = ur.role_id
WHERE ur.user_id = :user_id
"""

# Clients
GET_CLIENT_BY_EMAIL = """
SELECT * FROM clients WHERE email = :email
"""


GET_USER_BY_EMAIL = """
SELECT * FROM users WHERE email = :email
"""

GET_USER_BY_ID = """
SELECT * FROM users WHERE id = :user_id
"""

GET_USER_ROLES = """
SELECT r.role
FROM roles r
JOIN user_roles ur ON r.id = ur.role_id
WHERE ur.user_id = :user_id
"""

GET_CLIENT_BY_EMAIL = """
SELECT * FROM clients WHERE email = :email
"""

INSERT_USER = """
INSERT INTO users (name, email, location, status_id, created_by)
VALUES (:name, :email, :location, :status_id, :created_by)
"""

INSERT_USER_ROLE = """
INSERT INTO user_roles (user_id, role_id, assigned_by)
VALUES (:user_id, :role_id, :assigned_by)
"""



# _____________________________________________________

# app/sql/queries.py

# ------------------------------
# User Queries
# ------------------------------

# Get user by email
GET_USER_BY_EMAIL = """
SELECT *
FROM users
WHERE email = :email
"""

# Get user by ID
GET_USER_BY_ID = """
SELECT *
FROM users
WHERE id = :user_id
"""

# Insert new user (pending by default, no password)
INSERT_USER = """
INSERT INTO users (name, email, location, status_id, created_by)
VALUES (:name, :email, :location, :status_id, :created_by)
"""

# Update user password and enable MFA
UPDATE_USER_PASSWORD_MFA = """
UPDATE users
SET password_hash = :password_hash,
    mfa_secret = :mfa_secret,
    mfa_enabled = :mfa_enabled,
    status_id = 2  -- active after first login
WHERE id = :user_id
"""

# ------------------------------
# Role Queries
# ------------------------------

# Assign role to user
INSERT_USER_ROLE = """
INSERT INTO user_roles (user_id, role_id, assigned_by)
VALUES (:user_id, :role_id, :assigned_by)
"""

# Get roles of a user
GET_USER_ROLES = """
SELECT r.role
FROM roles r
JOIN user_roles ur ON ur.role_id = r.id
WHERE ur.user_id = :user_id
"""

# ------------------------------
# Client Queries (optional)
# ------------------------------

GET_CLIENT_BY_EMAIL = """
SELECT *
FROM clients
WHERE email = :email
"""
