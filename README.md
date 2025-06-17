# AI Semantic Code Refactorer

An intelligent web application that uses AI to analyze and refactor code, making it more maintainable and efficient.

## Project Overview

This project aims to create a web-based tool that can:
- Analyze code semantically
- Suggest meaningful refactoring opportunities
- Provide explanations for suggested changes
- Support multiple programming languages
- Learn from user feedback

## Development Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- Node.js 16+
- Git
- Your favorite code editor

### Getting Started

1. Clone the repository:
```bash
git clone [repository-url]
cd semantic-code-refactorer
```

2. Set up the backend:
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. Set up PostgreSQL:
```bash
# Create database
createdb code_refactorer
```

4. Configure environment variables:
Create a `.env` file in the project root:
```
DATABASE_URL=postgresql://postgres:6865@localhost:5432/code_refactorer
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
FRONTEND_URL=http://localhost:3000
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Set up the frontend:
```bash
cd frontend
npm install
```

7. Start development servers:
```bash
# Terminal 1 - Backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Project Structure

```
semantic-code-refactorer/
├── alembic/              # Database migrations
├── app/                  # Backend application
│   ├── core/            # Core functionality
│   │   ├── config.py    # Configuration settings
│   │   └── database.py  # Database connection
│   ├── models/          # Database models
│   │   └── code_refactoring.py  # SQLAlchemy models
│   ├── schemas/         # Pydantic models
│   └── main.py         # FastAPI application
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/      # Page components
│   │   └── services/   # API services
│   └── public/         # Static files
└── tests/              # Test files
```

## Database Models

- `CodeRefactoring`: Stores code refactoring requests and results
  - Original and refactored code
  - Explanation of changes
  - Status tracking
  - Timestamps

- `RefactoringFeedback`: Stores user feedback
  - Ratings and comments
  - Links to refactoring requests
  - Timestamps

## API Documentation

Once the backend is running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.