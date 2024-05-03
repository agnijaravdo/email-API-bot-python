from unittest.mock import patch
import pytest
from daily_newsletter import (
    validate_email_address,
    get_data_from_api_providers,
    update_newsletter_with_api_data,
    main,
)


def test_validate_email_address():
    with pytest.raises(SystemExit):
        validate_email_address("test.com")


def test_get_data_from_api_providers_wikimedia():
    result = get_data_from_api_providers("wikimedia")
    assert result[1] == "wikimedia"


def test_get_data_from_api_providers_jokes():
    result = get_data_from_api_providers("jokes")
    assert result[1] == "jokes"


def test_get_data_from_api_providers_invalid():
    with pytest.raises(SystemExit):
        get_data_from_api_providers("invalid")


def test_update_newsletter_with__wikimedia_api_data():
    data = "1990: Person One, an artist\n1980: Person Two, a scientist\n1970: Person Three, a musician"
    provider = "wikimedia"
    result = update_newsletter_with_api_data(data, provider)
    assert "1990: Person One, an artist" in result
    assert "1980: Person Two, a scientist" in result
    assert "1970: Person Three, a musician" in result


def test_update_newsletter_with__jokes_api_data():
    data = "What's a cat's favorite instrument? Purr-cussion"

    provider = "jokes"
    result = update_newsletter_with_api_data(data, provider)
    assert data in result


def test_update_newsletter_with_api_data_more_texts_than_tags():
    data = "1990: Person One, an artist\n1980: Person Two, a scientist\n1970: Person Three, a musician\n1960: Person Four, a writer"
    provider = "wikimedia"
    with pytest.raises(ValueError):
        update_newsletter_with_api_data(data, provider)


def test_main_missing_command_line_arguments():
    with patch("sys.argv", [""]):
        with pytest.raises(SystemExit):
            main()


def test_main_not_missing_command_line_arguments():
    with patch("sys.argv", ["daily_newsletter.py", "test@gmail.com", "wikimedia"]):
        with patch("daily_newsletter.send_an_email") as mock_send_an_email:
            main()
            mock_send_an_email.assert_called_once()
