# AI Semantic Code Refactorer

An intelligent web application that uses AI to analyze and refactor code, making it more maintainable and efficient.

## Project Overview

This project provides a robust backend service for AI-powered code analysis and refactoring.

**Core Features:**
- **Asynchronous Code Refactoring**: Submit code and get a refactored version with a detailed explanation.
- **Code Analysis**: Get a quality report on your code, including complexity and readability scores.
- **Improvement Suggestions**: Receive specific, actionable suggestions to improve your code.
- **Code Explanation**: Get a detailed, human-readable explanation of what a piece of code does.
- **Mock Service Included**: Run and test the full API without needing an AI provider API key.
- **Database Migrations**: Uses Alembic to manage the database schema.
- **Async API**: Built with FastAPI for high performance.

## Development Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- Node.js 16+ (for future frontend work)
- Git

### Getting Started

1.  **Clone the repository:**
    ```bash
    git clone [repository-url]
    cd semantic-code-refactorer
    ```

2.  **Set up the backend:**
    ```bash
    # Create and activate virtual environment
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate

    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Set up PostgreSQL:**
    ```bash
    # Create a new database
    createdb code_refactorer
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the project root. You can leave `OPENAI_API_KEY` blank to use the mock service.
    ```
    DATABASE_URL=postgresql://postgres:your_password@localhost:5432/code_refactorer
    SECRET_KEY=a-very-secret-key
    OPENAI_API_KEY=
    FRONTEND_URL=http://localhost:3000
    ```

5.  **Run Database Migrations:**
    ```bash
    alembic upgrade head
    ```

6.  **Start the Backend Server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

### Running Tests
To ensure everything is working correctly, run the test suite:
```bash
pytest
```

## API Documentation

Once the backend is running, interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Main Endpoints

-   `POST /api/refactoring/`: Submit code for refactoring. This is an asynchronous operation.
-   `GET /api/refactoring/{refactoring_id}`: Check the status and retrieve the result of a refactoring request.
-   `POST /api/refactoring/analyze`: Analyze a piece of code and receive a quality report.
-   `POST /api/refactoring/suggestions`: Get a list of specific improvement suggestions for your code.
-   `POST /api/refactoring/explain`: Get a detailed explanation of what a piece of code does.

## Project Structure

```
semantic-code-refactorer/
├── alembic/              # Database migrations
├── app/                  # Backend FastAPI application
│   ├── core/             # Core functionality (config, database)
│   ├── models/           # SQLAlchemy database models
│   ├── schemas/          # Pydantic data models
│   ├── services/         # Business logic (AI and mock services)
│   ├── routes/           # API endpoint definitions
│   └── main.py           # Main FastAPI app entrypoint
├── frontend/             # (Placeholder) React/Next.js frontend
└── tests/                # Pytest test suite
```

## Contributing

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

## License

This project is licensed under the MIT License.