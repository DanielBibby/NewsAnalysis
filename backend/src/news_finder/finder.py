from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()
news_api_key = os.getenv("NEWS_API_KEY")


class NewsFinder(BaseModel):
    start_date: str
    end_date: str
    company: str
    additional: List[str] = []

    def _create_url(self) -> str:
        """
        Using class attributes, create a URL to pass in a request.

        :return: URL string
        """
        if not news_api_key:
            raise ValueError(
                "API key not found. Make sure it's set in the environment variables."
            )

        base_url = "https://newsapi.org/v2/everything"
        query = f"{self.company}"
        if self.additional:
            query += f" {' '.join(self.additional)}"  # Add optional arguments

        params = {
            "q": query,
            "from": self.start_date,
            "to": self.end_date,
            "sortBy": "relevance",
            "apiKey": news_api_key,
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
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch articles. HTTP Status: {response.status_code}, Response: {response.text}"
            )

        articles = response.json().get("articles", [])
        total_articles = response.json().get("totalResults", 0)

        return articles, total_articles
