import sys
import os
import datetime
import requests
import smtplib
from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs

email = sys.argv[1]
api_provider = sys.argv[2]
possible_api_providers = ["wikimedia", "jokes"]
load_dotenv()


def validate_email_address(email):
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        sys.exit(str(e))


def get_wikimedia_response():
    today = datetime.datetime.now()
    date = today.strftime("%m/%d")
    url = "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/births/" + date

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
            events = []
            for i in range(min(3, len(data["births"]))):
                event_text = data["births"][i]["text"]
                year = data["births"][i]["year"]
                events.append(f"{year}: {event_text}")
            return "\n".join(events)
        else:
            return "The 'births' data is not found or not available."
    else:
        return "Failed to fetch data: HTTP status code " + str(response.status_code)


def get_jokes_response():
    url = "https://icanhazdadjoke.com/"

    headers = {"Accept": "text/plain"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        return "Failed to fetch data:", response.status_code


def get_data_from_api_providers(api_provider):
    if api_provider == "wikimedia":
        wikimedia_response = get_wikimedia_response()
        return wikimedia_response, api_provider
    elif api_provider == "jokes":
        jokes_response = get_jokes_response()
        return jokes_response, api_provider
    else:
        sys.exit(
            f"There is no data for provided API provider. Choose one from {possible_api_providers}"
        )


def update_newsletter_with_api_data(data, provider):
    html_file_path = f"data/{provider}_newsletter_template.html"
    base = os.path.dirname(os.path.abspath(__file__))
    html = open(os.path.join(base, html_file_path))
    soup = bs(html, "lxml")

    new_texts = data.splitlines()

    old_h2_tags = soup.find_all("h2")

    if len(old_h2_tags) < len(new_texts):
        raise ValueError("There are more texts to update than available <h2> tags")

    for index in range(len(new_texts)):
        old_h2_tags[index].string += new_texts[index]
    
    return str(soup)


def send_an_email(newsletter_message):
    APP_PASSWORD = os.getenv("APP_PASSWORD")
    msg = EmailMessage()
    msg['Subject'] = 'Your daily newsletter!'
    msg['From'] = email
    msg['To'] = email

    msg.set_content(newsletter_message, subtype='html')
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    try:
        s.login(email, APP_PASSWORD)
    except smtplib.SMTPAuthenticationError as e:
        sys.exit(f"Email Authentication is not possible. Error: {e}")
    s.send_message(msg)
    print("Email sent successfully!")


def main():
    if len(sys.argv) != 3:
        sys.exit(
            "Missing command line argument. You need to provide an email address and API to use"
        )

    validate_email_address(email)
    data, provider = get_data_from_api_providers(api_provider)
    print("Api data: ", data)
    print("Api provider: ", provider)
    newsletter_message = update_newsletter_with_api_data(data, provider)
    send_an_email(newsletter_message)

if __name__ == "__main__":
    main()
