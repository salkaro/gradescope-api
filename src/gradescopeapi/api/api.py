from fastapi import Depends, FastAPI, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware


from .._config.config import LoginRequestModel
from ..classes.account import Account
from ..classes.connection import GSConnection
from ..classes.courses import Course

# import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://unihub.salkaro.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create instance of GSConnection, to be used where needed
connection = GSConnection()


def get_gs_connection():
    """
    Returns the GSConnection instance

    Returns:
        connection (GSConnection): an instance of the GSConnection class,
            containing the session object used to make HTTP requests,
            a boolean defining True/False if the user is logged in, and
            the user's Account object.
    """
    return connection


def get_gs_connection_session():
    """
    Returns session of the the GSConnection instance

    Returns:
        connection.session (GSConnection.session): an instance of the GSConnection class' session object used to make HTTP requests
    """
    return connection.session


def get_account():
    """
    Returns the user's Account object

    Returns:
        Account (Account): an instance of the Account class, containing
            methods for interacting with the user's courses and assignments.
    """
    return Account(session=get_gs_connection_session)


# Create instance of GSConnection, to be used where needed
connection = GSConnection()

account = None


@app.get("/")
def root():
    return {"message": "Welcome to gradescope api"}


@app.post("/login", name="login")
def login(
    login_data: LoginRequestModel,
    gs_connection: GSConnection = Depends(get_gs_connection),
):
    """Login to Gradescope, with correct credentials

    Args:
        username (str): email address of user attempting to log in
        password (str): password of user attempting to log in

    Raises:
        HTTPException: If the request to login fails, with a 404 Unauthorized Error status code and the error message "Account not found".
    """
    user_email = login_data.email
    password = login_data.password

    try:
        connection.login(user_email, password)
        global account
        account = connection.account
        return {"message": "Login successful", "status_code": status.HTTP_200_OK}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"Account not found. Error {e}")


@app.post("/courses", response_model=dict[str, dict[str, Course]])
def get_courses():
    """Get all courses for the user

    Args:
        account (Account): Account object containing the user's courses

    Returns:
        dict: dictionary of dictionaries

    Raises:
        HTTPException: If the request to get courses fails, with a 500 Internal Server Error status code and the error message.
    """
    try:
        course_list = account.get_courses()
        return course_list
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/assignments")
def get_assignments(course_id: str = Body(..., embed=True)):
    """Get all assignments for a course

    Args:
        course_id: ID of a course

    Returns:
        dict: dictionary of course information
    """
    try:
        assignments = account.get_assignments(course_id)
        return assignments
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


# if __name__ == "__main__":
# uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
