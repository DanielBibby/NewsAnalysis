from pydantic import BaseModel, SecretStr
from typing import List, Optional
from dotenv import load_dotenv
import os
import requests

# Load environment variables, used for those who cloned the repo from GitHub
load_dotenv()


class APIException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class NewsFinder(BaseModel):
    start_date: str
    end_date: str
    company: str
    additional: List[str] = []
    api_key: Optional[SecretStr] = None

    def _create_url(self) -> str:
        """
        Using class attributes, create a URL to pass in a request.

        :return: URL string
        """
        if not self.api_key:
            self.api_key = os.getenv("NEWS_API_KEY")
            if not self.api_key:
                raise APIException(
                    "API key not found. Make sure it's entered above (or in the .env file if you cloned from GitHub)."
                )

        base_url = "https://newsapi.org/v2/everything"
        query = f"{self.company}"
        if self.additional:
            query += f" {' '.join(self.additional)}"  # Add optional arguments

        params = {
            "q": query,
            "from": self.start_date,
            "to": self.end_date,
            "sortBy": "popularity",
            "apiKey": self.api_key.get_secret_value(),
            "language": "en",
            "searchIn": "title",
        }

        # Construct URL with query parameters
        query_string = "&".join(f"{key}={value}" for key, value in params.items())
        return f"{base_url}?{query_string}"

    def get_articles(self) -> (List[dict], int):
        """
        Make an API request to get articles.

        :return: List of articles
        """
        url = self._create_url()
        response = requests.get(url)
        if response.status_code == 403:
            raise APIException("Invalid API Key")
        elif response.status_code != 200:
            raise APIException(
                f"Failed to fetch articles. HTTP Status: {response.status_code}, Response: {response.text}"
            )

        articles = response.json().get("articles", [])
        total_articles = response.json().get("totalResults", 0)

        return articles, total_articles
