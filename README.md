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
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Start development servers:
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
├── app/                    # Backend application
│   ├── api/               # API endpoints
│   ├── core/              # Core functionality
│   ├── models/            # Database models
│   └── services/          # Business logic
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Page components
│   │   └── services/     # API services
│   └── public/           # Static files
└── tests/                # Test files
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 