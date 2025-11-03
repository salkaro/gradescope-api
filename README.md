# Gradescope API

[![PyPI - Version](https://img.shields.io/pypi/v/gradescopeapi)](https://pypi.org/project/gradescopeapi/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gradescopeapi) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nyuoss/gradescope-api/.github%2Fworkflows%2Fmain.yaml)

## Description

This *unofficial* project serves as a library for programmatically interacting with [Gradescope](https://www.gradescope.com/). The primary purpose of this project is to provide students and instructors tools for interacting with Gradescope without having to use the web interface.

### Use Cases

- **Students:** Automatically query information about courses and assignments to notify them of upcoming deadlines or new assignments.
- **Instructors:** Bulk edit assignment due dates, manage student extensions, or sync data with external systems.
- **Developers:** Build integrations and tools that leverage Gradescope data (e.g., academic dashboards, assignment trackers, etc.)

### Technology Stack

- **Python 3.10+**
- **FastAPI 0.120.4** - REST API server
- **Requests 2.32.5** - HTTP client for Gradescope communication
- **BeautifulSoup4 4.14.2** - Web scraping and HTML parsing
- **Pydantic 2.12.3** - Data validation and serialization
- **Uvicorn 0.38.0** - ASGI server
- **Vercel** - Serverless deployment platform

## Features

### Core Functionality

- **Course Management**
  - Get all courses for a user (instructor and student roles)
  - Retrieve course roster/members with details

- **Assignment Operations**
  - Get a list of all assignments for a course
  - Add/remove/modify dates for an assignment (release, due, late submission)
  - Get assignment submissions and graders
  - Upload submissions to assignments

- **Extension Management**
  - Get all extensions for an assignment in a course
  - Add/remove/modify student extensions for assignments

- **API Server**
  - FastAPI REST server to interact with library without Python
  - Auto-generated API documentation (Swagger UI)
  - CORS support for cross-origin requests

## Demo

To get a feel for how the API works, we have provided a demo video of the features in-use: [link](https://youtu.be/eK9m4nVjU1A?si=6GTevv23Vym0Mu8V)

Note that we only demo interacting with the API server, you can alternatively use the Python library directly.

## Setup

To use the project you can install the package from PyPI using pip:

```bash
pip install gradescopeapi
```

For additional methods of installation, refer to the [install guide](docs/INSTALL.md)

## Usage

The project is designed to be simple and easy to use. As such, we have provided users with two different options for using this project.

### Option 1: FastAPI Server

If you do not want to use Python, you can host the API using the integrated FastAPI server. This way, you can interact with Gradescope using different languages by sending HTTP requests to the API server.

**Running the API Server Locally**

To run the API server locally on your machine, open the project repository on your machine that you have cloned/forked, and:

1. Navigate to the `src.gradescopeapi.api` directory
1. Run the command: `uvicorn api:app --reload` to run the server locally
1. In a web browser, navigate to `localhost:8000/docs`, to see the auto-generated FastAPI docs

**Available API Endpoints**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Root/welcome message |
| `/login` | POST | Authenticate user with email and password |
| `/courses` | POST | Fetch all courses for authenticated user |
| `/assignments` | POST | Fetch assignments for a specific course |

**Deployment**

The API is configured for deployment on Vercel as a serverless function. See [vercel.json](vercel.json) for configuration details.

### Option 2: Python

Alternatively, you can use Python to use the library directly. We have provided some sample scripts of common tasks one might do:

```python
from gradescopeapi.classes.connection import GSConnection

# create connection and login
connection = GSConnection()
connection.login("email@domain.com", "password")

"""
Fetching all courses for user
"""
courses = connection.account.get_courses()
for course in courses["instructor"]:
    print(course)
for course in courses["student"]:
    print(course)

"""
Getting roster for a course
"""
course_id = "123456"
members = connection.account.get_course_users(course_id)
for member in members:
    print(member)

"""
Getting all assignments for course
"""
assignments = connection.account.get_assignments(course_id)
for assignment in assignments:
    print(assignment)
```

For more examples of features not covered here such as changing extensions, uploading files, etc., please refer to the [tests](tests/) directory.

## Testing

For information on how to run your own tests using `gradescopeapi`, refer to [TESTING.md](docs/TESTING.md)

## Contributing Guidelines

Please refer to the [CONTRIBUTING.md](docs/CONTRIBUTING.md) file for more information on how to contribute to the project.

## Authors

- Susmitha Kusuma
- Berry Liu
- Margaret Jagger
- Calvin Tian
- Kevin Zheng
