# Backend Engineering Challenge - E-commerce Microservices System

## Introduction

This project implements a microservices-based e-commerce system managing user authentication, product management, and order processing. The system ensures concurrency control, high availability, and database integration. This README provides setup instructions, architectural details, and additional information for running the project.

## Table of Contents

- [Introduction](#introduction)
- [Architecture](#architecture)
- [Services](#services)
- [Concurrency Control](#concurrency-control)
- [Clustering and High Availability](#clustering-and-high-availability)
- [Database Integration](#database-integration)
- [APIs and Communication](#apis-and-communication)
- [Authentication and Authorization](#authentication-and-authorization)
- [Setup Instructions](#setup-instructions)
- [Testing](#testing)
- [Bonus Features](#bonus-features)
- [Assumptions](#assumptions)

## Architecture

The system is divided into three core microservices:

1. **User Authentication Service**: Manages user registration, login, and authentication.
2. **Product Management Service**: Handles CRUD operations for products.
3. **Order Processing Service**: Manages order creation, updates, and history.

Each service is containerized using Docker and deployed on Kubernetes for high availability and scalability.

## Services

### User Authentication Service

- **Endpoints**:
  - `POST /register`: Register a new user
  - `POST /login`: User login
  - `GET /profile`: Get user profile (protected)
- **Features**:
  - JWT-based authentication
  - Secure password storage with bcrypt

### Product Management Service

- **Endpoints**:
  - `POST /products/create_product`: Create a new product
  - `GET /products/`: Get a list of products
  - `GET /products/:id`: Get product details
  - `PUT /products/:id`: Update product information
  - `DELETE /products/:id`: Delete a product
- **Concurrency Control**:
  - Optimistic locking using versioning to prevent data conflicts

### Order Processing Service

- **Endpoints**:
  - `POST /orders/create_order`: Create a new order
  - `GET /orders`: Get a list of orders
  - `GET /orders/:id`: Get order details
  - `PUT /orders/:id`: Update order status
  - `DELETE /orders/:id`: Cancel an order
- **Features**:
  - Users can create and manage their own orders

## Concurrency Control

- **Optimistic Locking**: Implemented in the Product Management Service to prevent conflicts during concurrent updates. Each product has a `version` field checked and incremented on updates.

## Clustering and High Availability
0
- **Kubernetes**: Services are deployed as Kubernetes Deployments with multiple replicas for high availability.
- **NGINX**: Used as an Ingress controller for load balancing.

## Database Integration

- **MongoDB**: Used for storing user information, product data, and order history.
- **Schema Design**:
  - User: `{ userId, username, email, passwordHash }`
  - Product: `{ productId, name, description, price, stock, version }`
  - Order: `{ orderId, userId, productList, totalAmount, status, createdAt }`

## APIs and Communication

- **RESTful APIs**: Each microservice exposes RESTful endpoints.
- **Synchronous Communication**: Services communicate via HTTP requests.

## Authentication and Authorization

- **JWT**: Used for secure user authentication. Protected endpoints require a valid JWT.

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose
- Kubernetes (Minikube or any Kubernetes cluster)
- kubectl

### Steps

1. **Clone the repository**:
   ```sh
   git clone <repository-url>
   cd project-directory
