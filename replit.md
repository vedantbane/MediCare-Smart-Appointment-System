# Overview

MediCare is a web-based appointment management system built with Flask that facilitates scheduling and management of medical appointments between patients and doctors. The application provides role-based functionality with separate interfaces for patients to book appointments and doctors to manage their schedules and view patient appointments.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Framework
The application uses Flask as the primary web framework with SQLAlchemy for database operations. The architecture follows a traditional MVC pattern with clear separation between models, routes (controllers), and templates (views).

## Database Design
The system uses SQLAlchemy ORM with a declarative base model approach. The database supports both SQLite (for development) and can be configured for production databases through environment variables. Key entities include:
- **User Model**: Handles both patients and doctors with role-based differentiation
- **Appointment Model**: Manages booking relationships between patients and doctors
- **DoctorSchedule Model**: Manages doctor availability and scheduling

## Authentication System
User authentication is implemented using Flask sessions with Werkzeug's password hashing utilities. The system includes:
- Password hashing for secure storage
- Session management for user state
- Role-based access control (patient vs doctor)
- Login required decorators for protected routes

## Frontend Architecture
The frontend uses a modern stack with:
- **Tailwind CSS**: For responsive design and styling
- **Font Awesome**: For iconography
- **Custom CSS**: For animations and enhanced user experience
- **Jinja2 Templates**: For server-side rendering

## Application Structure
The codebase is organized into distinct modules:
- `app.py`: Application configuration and initialization
- `models.py`: Database models and relationships
- `routes.py`: URL routing and request handling
- `main.py`: Application entry point
- `templates/`: HTML templates
- `static/`: CSS and static assets

## Security Features
- Environment-based configuration for sensitive data
- Password hashing using Werkzeug security utilities
- Session-based authentication
- CSRF protection through Flask's built-in mechanisms
- ProxyFix middleware for proper header handling in production

# External Dependencies

## Core Framework Dependencies
- **Flask**: Web application framework
- **Flask-SQLAlchemy**: Database ORM integration
- **Werkzeug**: Security utilities for password hashing and proxy handling

## Frontend Dependencies
- **Tailwind CSS**: Utility-first CSS framework (CDN)
- **Font Awesome**: Icon library (CDN)
- **Google Fonts**: Poppins font family for typography

## Database
- **SQLite**: Default development database
- **Configurable Database**: Production-ready through DATABASE_URL environment variable

## Development Tools
- **Python Logging**: Built-in logging for debugging and monitoring
- **Flask Debug Mode**: Development server with hot reloading

## Environment Configuration
The application relies on environment variables for:
- `SESSION_SECRET`: Session encryption key
- `DATABASE_URL`: Database connection string