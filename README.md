# SQLAlchemy ORM Exercise Project

This project demonstrates the implementation of a database system using SQLAlchemy ORM, featuring a university-like course management system with relationships between students, professors, courses, and categories.

## Project Structure

The project implements the following models:
- `Student`: Represents students with personal information
- `Professor`: Represents professors and their teaching subjects
- `Course`: Represents courses with professor assignments and categories
- `Category`: Represents course categories with pricing
- `StudentCourse`: Junction table managing student enrollments and grades

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd orm_exercises
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your database configuration:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
```

## Database Setup

1. Create a PostgreSQL database
2. Update the `.env` file with your database credentials
3. The tables will be automatically created when you run the application

## Running the Application

To run the application and perform the demonstration operations:

```bash
python main.py
```

This will:
- Create all necessary database tables
- Insert sample data (5 records for each model)
- Perform update operations (2 records for each model)
- Perform delete operations (1 record for each model)

## Features

- Complete CRUD operations demonstration
- Relationship management between models
- Cascade delete operations
- Transaction management with rollback support
- Environment variable configuration

## Model Relationships

- Students can enroll in multiple courses (Many-to-Many)
- Professors can teach multiple courses (One-to-Many)
- Categories can have multiple courses (One-to-Many)
- Courses can have multiple students (Many-to-Many)

## Error Handling

The application includes error handling with:
- Transaction management
- Automatic rollback on failure
- Exception logging

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 