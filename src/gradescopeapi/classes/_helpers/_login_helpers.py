import requests
from bs4 import BeautifulSoup

from ...constants import DEFAULT_GRADESCOPE_BASE_URL


def get_auth_token_init_gradescope_session(
    session: requests.Session,
    gradescope_base_url: str = "https://www.gradescope.com",
) -> str | None:
    """
    Go to homepage to parse hidden authenticity token and set initial "_gradescope_session" cookie.
    """
    try:
        homepage_resp = session.get(gradescope_base_url, timeout=10)
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to reach Gradescope homepage: {e}")

    # Ensure we got a valid response
    if homepage_resp is None or homepage_resp.status_code != 200:
        raise RuntimeError(
            f"Unexpected response from Gradescope (status {getattr(homepage_resp, 'status_code', 'N/A')})"
        )

    # Create BeautifulSoup safely
    homepage_soup = BeautifulSoup(homepage_resp.text or "", "html.parser")
    if homepage_soup is None or homepage_soup.text.strip() == "":
        raise RuntimeError("Received empty or invalid HTML from Gradescope homepage")

    # Try to find the authenticity token
    auth_input = homepage_soup.select_one(
        'form[action="/login"] input[name="authenticity_token"]'
    )
    if auth_input is None:
        return None

    return auth_input["value"]


def login_set_session_cookies(
    session: requests.Session,
    email: str,
    password: str,
    auth_token: str,
    gradescope_base_url: str = DEFAULT_GRADESCOPE_BASE_URL,
) -> bool:
    GS_LOGIN_ENDPOINT = f"{gradescope_base_url}/login"

    # populate params for post request to login endpoint
    login_data = {
        "utf8": "✓",
        "session[email]": email,
        "session[password]": password,
        "session[remember_me]": 0,
        "commit": "Log In",
        "session[remember_me_sso]": 0,
        "authenticity_token": auth_token,
    }

    # login -> Send post request to login endpoint. Sets cookies
    login_resp = session.post(GS_LOGIN_ENDPOINT, params=login_data)

    # success marked with cookies set and a 302 redirect to the accounts page
    if (
        # login_resp.history returns a list of redirects that occurred while handling a request
        len(login_resp.history) != 0
        and login_resp.history[0].status_code == requests.codes.found
    ):
        # update headers with csrf token
        # grab x-csrf-token
        soup = BeautifulSoup(login_resp.text, "html.parser")
        csrf_token = soup.select_one('meta[name="csrf-token"]')["content"]

        # update session headers
        session.cookies.update(login_resp.cookies)
        session.headers.update({"X-CSRF-Token": csrf_token})
        return True
    return False
