import sys
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv
import os
import datetime
import requests

email = sys.argv[1]
api_provider = sys.argv[2]
possible_api_providers = ["wikimedia", "jokes"]


def validate_email_address(email):
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        sys.exit(str(e))


def get_wikimedia_response():
    today = datetime.datetime.now()
    date = today.strftime("%m/%d")
    url = "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/births/" + date

    load_dotenv()
    WIKIMEDIA_ACCESS_TOKEN = os.getenv("WIKIMEDIA_ACCESS_TOKEN")
    USER_EMAIL = os.getenv("USER_EMAIL")

    headers = {
        "Authorization": f"Bearer {WIKIMEDIA_ACCESS_TOKEN}",
        "User-Agent": USER_EMAIL,
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "births" in data and len(data["births"]) > 0:
            event_on_this_day = data["births"][0]

            event_on_this_day = data["births"][0]["text"]
            return event_on_this_day
        else:
            return "The 'births' data is not found or not available"
    else:
        return "Failed to fetch data:", response.status_code


def get_jokes_response():
    url = "https://icanhazdadjoke.com/"

    headers = {"Accept": "text/plain"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        return "Failed to fetch data:", response.status_code


def get_data_from_api_providers(api_provider):
    if api_provider == "wikimedia":
        wikimedia_response = get_wikimedia_response()
        print(wikimedia_response)
    elif api_provider == "jokes":
        jokes_response = get_jokes_response()
        print(jokes_response)
    else:
        print(
            f"There is no data for provided API provider. Choose one from {possible_api_providers}"
        )


def main():
    if len(sys.argv) != 3:
        sys.exit(
            "Missing command line argument. You need to provide an email address and API to use"
        )

    validate_email_address(email)
    get_data_from_api_providers(api_provider)


if __name__ == "__main__":
    main()
