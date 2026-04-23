#  Fullstack Social Network API

A high-performance social networking engine built with a focus on robust software architecture, relational data integrity, and secure stateless authentication. This project bridges a high-concurrency FastAPI backend with a modern, lightweight frontend.

## 🛠️ Technical Ecosystem

### Backend Architecture
* **FastAPI**: Leveraging asynchronous programming for high-performance I/O operations.
* **PostgreSQL**: Utilizing a relational schema for ACID-compliant data persistence and complex relationship mapping.
* **SQLAlchemy / Tortoise (ORM)**: Implementation of the Data Mapper/Active Record pattern for database abstraction.
* **Pydantic**: Strict data parsing and serialization using Python type hints.
* **JWT (JSON Web Tokens)**: Implementation of OAuth2 with Password hashing (Passlib/Bcrypt) for secure authorization.

### Frontend Engineering
* **Modern Vanilla JS**: Event-driven architecture for state management without the overhead of heavy frameworks.
* **Tailwind CSS**: Atomic CSS approach for rapid UI development and consistent design tokens.
* **Lucide Icons**: SVG-based iconography for optimized DOM rendering.

## ⚙️ Core Engineering Features

- [x] **Secure Authentication Flow**: Integrated Password Hashing (Bcrypt) and JWT-based session management.
- [x] **Relational Schema Design**: Structured User entities optimized for PostgreSQL indexing.
- [x] **API Resilience**: Global Exception Handling and standardized HTTP response codes.
- [x] **CORS & Security**: Strict middleware configuration for secure Cross-Origin Resource Sharing.
- [x] **Client-Side Security**: Dynamic DOM manipulation for sensitive data visibility (Password Toggle).

## Deployment & Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/XxSuarezxX/social-network.git

2. Backend Configuration:
    Initialize a virtual environment (venv).
    Install dependencies: pip install -r requirements.txt.
    Configure your PostgreSQL connection string in the environment variables.
    Run the development server: uvicorn main:app --reload.

3. Frontend Interaction:
    Serve the frontend directory via a static server (e.g., Live Server).
    Navigate to the entry point: auth/login/login.html.
