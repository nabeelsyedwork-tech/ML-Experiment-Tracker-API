# 🚀 ML Experiment Tracker API

A backend application built with **FastAPI**, **SQLAlchemy**, and **JWT Authentication** for managing machine learning projects and experiments in a secure, multi-user environment.

---

## Overview

Machine learning workflows often involve running multiple experiments with different parameters and evaluating their performance.

This project provides a centralized API that allows users to:

* Create and manage ML projects
* Track experiments within projects
* Store experiment parameters and metrics
* Secure data using JWT authentication
* Ensure users only access their own resources

---

## Features

### 🔐 Authentication & Authorization

* User Registration
* User Login
* JWT Access Tokens
* Password Hashing with Bcrypt
* Protected Endpoints
* User Ownership Validation

---

### 📁 Project Management

Users can:

* Create Projects
* Retrieve All Projects
* Retrieve a Specific Project
* Delete Projects

Each project is linked to its owner through database relationships.

---

### 🧪 Experiment Tracking

Users can:

* Create Experiments
* Store Parameters as JSON
* Store Metrics as JSON
* Retrieve All Experiments in a Project
* Retrieve Individual Experiments
* Delete Experiments

Experiments are organized under projects, enabling structured experiment management.

---

## Database Design

### User

Stores authentication and ownership information.

Fields:

* `userid`
* `username`
* `password`

---

### Project

Represents a machine learning project.

Fields:

* `projectid`
* `name`
* `userid`

Relationship:

* One User → Many Projects

---

### Experiment

Represents an individual experiment within a project.

Fields:

* `experimentid`
* `name`
* `params`
* `metrics`
* `projectid`

Relationship:

* One Project → Many Experiments

---

## API Structure

### Authentication

```http
POST /auth/register
POST /auth/login
GET  /auth/me
```

---

### Projects

```http
POST   /projects
GET    /projects
GET    /projects/{projectid}
DELETE /projects/{projectid}
```

---

### Experiments

```http
POST   /projects/{projectid}/experiments
GET    /projects/{projectid}/experiments
GET    /projects/{projectid}/experiments/{experimentid}
DELETE /projects/{projectid}/experiments/{experimentid}
```

---

## Architecture

The application follows a modular backend architecture:

```text
app/
│
├── core/
├── db/
├── schemas/
├── services/
├── dependencies/
├── routers/
└── main.py
```

### Components

* **Routers** → API Endpoints
* **Services** → Database Operations
* **Schemas** → Request & Response Validation
* **Models** → SQLAlchemy ORM Models
* **Dependencies** → Authentication Logic
* **Core** → Security & Configuration

---

## Security

Implemented using:

* JWT Authentication
* OAuth2 Password Flow
* Password Hashing (Bcrypt)
* User Ownership Checks
* Protected Routes

Users can only access projects and experiments that belong to them.

---

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* JWT (python-jose)
* Passlib (Bcrypt)
* Pydantic
* Uvicorn

---

## Configuration

Environment variables are managed through a `.env` file.

Example:

```env
DATABASE_URL=sqlite:///./FastAPI_test.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Future Improvements

Planned enhancements:

* Redis Caching
* Application Logging
* Docker Support
* PostgreSQL Integration
* Pagination
* Filtering
* Sorting
* Experiment Update Endpoints
* CI/CD Pipeline

---

## Key Takeaways

* Built a complete FastAPI backend from scratch
* Implemented JWT-based authentication and authorization
* Designed relational database models using SQLAlchemy
* Applied ownership-based access control
* Structured the application using a scalable modular architecture
* Developed a foundation for ML experiment management systems

---

## Project Status

✅ MVP Complete

The application provides secure user authentication, project management, experiment tracking, and a maintainable backend architecture suitable for further scaling and deployment.
