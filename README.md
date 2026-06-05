# 🚀 ML Experiment Tracker API

A production-ready backend application built with **FastAPI**, **SQLAlchemy**, **JWT Authentication**, **Redis Caching**, and **Docker** for managing machine learning projects and experiments in a secure multi-user environment.

---

## Overview

Machine learning workflows often involve running multiple experiments with different hyperparameters, tracking performance metrics, and comparing results across iterations.

This project provides a centralized API that allows users to:

* Create and manage machine learning projects
* Track experiments within projects
* Store experiment parameters and evaluation metrics
* Secure resources using JWT authentication
* Improve performance through Redis caching
* Deploy consistently using Docker and Docker Compose
* Query data efficiently using filtering, sorting, and pagination

---

## Features

### 🔐 Authentication & Authorization

* User Registration
* User Login
* JWT Access Tokens
* Password Hashing with Bcrypt
* Protected Endpoints
* Ownership-Based Access Control
* OAuth2 Password Flow

Users can only access projects and experiments that belong to them.

---

### 📁 Project Management

Users can:

* Create Projects
* Retrieve Projects
* Delete Projects
* Filter Projects by Name or ID
* Sort Results
* Paginate Results

---

### 🧪 Experiment Tracking

Users can:

* Create Experiments
* Store Parameters as JSON
* Store Metrics as JSON
* Retrieve Experiments
* Delete Experiments
* Filter Experiments by Name or ID
* Sort Results
* Paginate Results

Experiments are organized under projects, enabling structured experiment management and experiment history tracking.

---

### ⚡ Redis Caching

Implemented Redis caching for frequently accessed endpoints:

* Project Listings
* Experiment Listings

Benefits:

* Reduced database queries
* Faster response times
* Automatic cache invalidation after data modifications

---

### 📝 Application Logging

Structured logging is implemented for:

* Application startup events
* User registration and authentication events
* Project creation and deletion
* Experiment creation and deletion
* Cache hits and cache misses
* Warning and error events

Logs are written to both:

* Console
* Log Files

---

### 🐳 Dockerized Deployment

The application is fully containerized using:

* Docker
* Docker Compose

Services:

* FastAPI Application Container
* Redis Container

The entire application stack can be launched with a single command:

```bash
docker compose up --build
```

---

## Database Design

### User

Stores authentication and ownership information.

Fields:

* `userid`
* `username`
* `password`

Relationship:

* One User → Many Projects

---

### Project

Represents a machine learning project.

Fields:

* `projectid`
* `name`
* `userid`

Relationship:

* One Project → Many Experiments

---

### Experiment

Represents an individual experiment.

Fields:

* `experimentid`
* `name`
* `params`
* `metrics`
* `projectid`

Parameters and metrics are stored as JSON objects, allowing flexible experiment tracking.

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
DELETE /projects/{projectid}
DELETE /projects
```

Supported Query Parameters:

```http
GET /projects?project_name=XGB-Fraud-Model
GET /projects?sort_by=name&order=asc
GET /projects?page=1&limit=10
```

---

### Experiments

```http
POST   /projects/{projectid}/experiments
GET    /projects/{projectid}/experiments
DELETE /projects/{projectid}/experiments/{experimentid}
DELETE /projects/{projectid}/experiments
```

Supported Query Parameters:

```http
GET /projects/1/experiments?experiment_name=XGB-V1
GET /projects/1/experiments?sort_by=name&order=desc
GET /projects/1/experiments?page=1&limit=10
```

---

## Architecture

The application follows a modular backend architecture.

```text
app/
│
├── cache/
├── core/
├── db/
├── dependencies/
├── logs/
├── routers/
├── schemas/
├── services/
└── main.py
```

### Components

* Routers → API Endpoints
* Services → Database Logic
* Schemas → Validation & Serialization
* Models → SQLAlchemy ORM Models
* Dependencies → Authentication Dependencies
* Core → Configuration & Security
* Cache → Redis Integration

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite

### Authentication

* JWT (python-jose)
* Passlib (Bcrypt)

### Data Validation

* Pydantic

### Caching

* Redis

### Deployment

* Docker
* Docker Compose

### Logging

* Python Logging

### Server

* Uvicorn

---

## Configuration

Environment variables are managed through a `.env` file.

Example:

```env
DATABASE_URL=sqlite:///./fastapi.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

REDIS_HOST=redis
REDIS_PORT=6379

LOG_LEVEL=INFO
```

---

## Running the Project

### Local Development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

### Docker Deployment

```bash
docker compose up --build
```

API Documentation:

```text
http://localhost:8000/docs
```

---

## Key Takeaways

Through this project, I gained hands-on experience with:

* REST API Development using FastAPI
* JWT Authentication & Authorization
* SQLAlchemy ORM & Relational Database Design
* Ownership-Based Access Control
* Redis Caching Strategies
* Application Logging
* Docker Containerization
* Docker Compose Orchestration
* Filtering, Sorting, and Pagination
* Modular Backend Architecture

---

## Project Status

✅ Complete

The application provides a secure, containerized, and scalable backend system for managing machine learning projects and experiments. It demonstrates core backend engineering concepts including authentication, caching, logging, API design, database modeling, and deployment.
