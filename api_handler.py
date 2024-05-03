import os
import datetime
import requests
from dotenv import load_dotenv

load_dotenv()


def get_response(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch data: {e}")
    return response


def get_wikimedia_response():
    today = datetime.datetime.now()
    date = today.strftime("%m/%d")
    url = f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/births/{date}"

    headers = {
        "Authorization": f"Bearer {os.getenv("WIKIMEDIA_ACCESS_TOKEN")}",
        "User-Agent": os.getenv("USER_EMAIL"),
    }

    response = get_response(url, headers=headers)
    data = response.json()

    if "births" in data and len(data["births"]) > 2:
        events = []
        for i in range(min(3, len(data["births"]))):
            event_text = data["births"][i]["text"]
            year = data["births"][i]["year"]
            events.append(f"{year}: {event_text}")
        return "\n".join(events)
    else:
        raise Exception("The 'births' data is not found or not available.")


def get_jokes_response():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "text/plain"}

    response = get_response(url, headers=headers)
    return response.content.decode("utf-8")
