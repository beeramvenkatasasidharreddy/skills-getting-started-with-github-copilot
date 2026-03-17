# Tests

This directory contains backend tests for the FastAPI application.

## Running Tests

```bash
# Install dependencies (including pytest)
pip install -r requirements.txt

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::test_signup_successful
```

## Test Coverage

The tests cover:

- **GET /** - Root redirect to static index
- **GET /activities** - Retrieve all activities
- **POST /activities/{activity_name}/signup** - Student signup (success and error cases)
- **DELETE /activities/{activity_name}/unregister/{email}** - Student unregistration (success and error cases)

Error cases tested include:
- Non-existent activities
- Duplicate registrations
- Unregistering when not registered