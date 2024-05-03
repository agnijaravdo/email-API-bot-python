import os
from unittest.mock import Mock, patch
from api_handler import get_response, get_jokes_response, get_wikimedia_response

births_data = {
    "births": [
        {"year": "1990", "text": "Person One, an artist"},
        {"year": "1980", "text": "Person Two, a scientist"},
        {"year": "1970", "text": "Person Three, a musician"},
    ]
}
joke = "What's a cat's favorite instrument? Purr-cussion"


@patch("api_handler.requests.get")
def test_get_wikimedia_response_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = births_data
    mock_get.return_value = mock_response

    result = get_wikimedia_response()
    expected_result = "1990: Person One, an artist\n1980: Person Two, a scientist\n1970: Person Three, a musician"
    assert result == expected_result


@patch("api_handler.requests.get")
def test_get_wikimedia_response_failure(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    try:
        get_wikimedia_response()
    except Exception as e:
        assert str(e) == "The 'births' data is not found or not available."


@patch("api_handler.requests.get")
def test_get_jokes_response_success(mock_get):
    mock_response = Mock()
    mock_response.content = joke.encode("utf-8")
    mock_get.return_value = mock_response

    result = get_jokes_response()
    assert result == joke


@patch("api_handler.requests.get")
def test_get_jokes_response_failure(mock_get):
    mock_response = Mock()
    mock_response.content = b""
    mock_get.return_value = mock_response

    try:
        get_jokes_response()
    except Exception as e:
        assert str(e) == "Failed to fetch data: b''"


@patch("api_handler.requests.get")
def test_get_response_success(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_response("https://example.com", {})
    assert result == mock_response


@patch("api_handler.requests.get")
def test_get_response_failure(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("Failed to fetch data")
    mock_get.return_value = mock_response

    try:
        get_response("https://example.com", {})
    except Exception as e:
        assert str(e) == "Failed to fetch data"


def test_env_vars():
    assert os.getenv("WIKIMEDIA_ACCESS_TOKEN") is not None
    assert os.getenv("USER_EMAIL") is not None
