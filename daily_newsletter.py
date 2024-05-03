import sys
import os
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
from api_handler import get_jokes_response, get_wikimedia_response
from email_handler import send_an_email


def validate_email_address(email):
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        sys.exit(f"Provided email address is not valid. Try again. Error: {e}")


def get_data_from_api_providers(api_provider):
    if api_provider == "wikimedia":
        wikimedia_response = get_wikimedia_response()
        return wikimedia_response, api_provider
    elif api_provider == "jokes":
        jokes_response = get_jokes_response()
        return jokes_response, api_provider
    else:
        sys.exit(
            f"There is no data for provided API provider. Choose 'wikimedia' or 'jokes'"
        )


def update_newsletter_with_api_data(data, provider):
    html_file_path = f"templates/{provider}_newsletter_template.html"
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, html_file_path)) as html:
        soup = bs(html, "lxml")

    new_h2_tags_texts = data.splitlines()

    old_h2_tags = soup.find_all("h2")

    if len(old_h2_tags) < len(new_h2_tags_texts):
        raise ValueError("There are more texts to update than available <h2> tags")

    for index in range(len(new_h2_tags_texts)):
        old_h2_tags[index].string += new_h2_tags_texts[index]

    return str(soup)


def main():
    if len(sys.argv) != 3:
        sys.exit(
            "Missing command line argument. You need to provide an email address and API to use"
        )

    email = sys.argv[1]
    api_provider = sys.argv[2]

    validate_email_address(email)
    data, provider = get_data_from_api_providers(api_provider)

    newsletter_message = update_newsletter_with_api_data(data, provider)
    response = send_an_email(email, newsletter_message)
    print(response)

if __name__ == "__main__":
    main()
