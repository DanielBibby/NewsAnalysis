import pandas as pd
from pydantic import BaseModel, SecretStr
from typing import List, Optional

from backend.src.sentiment_analysis.analysis import SentimentAnalysis
from backend.src.news_finder.finder import NewsFinder

import logging


class BaseAnalysisChain(BaseModel):
    company: str
    start_date: str
    end_date: str
    additional: List[str] = []
    api_key: Optional[SecretStr] = None

    news_finder: Optional[NewsFinder] = None
    sentiment_analysis: SentimentAnalysis = SentimentAnalysis()

    def __init__(
        self,
        company: str,
        start_date: str,
        end_date: str,
        additional: List[str] = [],
        api_key: Optional[SecretStr] = None,
    ):
        super().__init__(
            company=company,
            start_date=start_date,
            end_date=end_date,
            additional=additional,
            api_key=api_key,
        )

        self.company = company
        self.start_date = start_date
        self.end_date = end_date
        self.additional = additional

        self.news_finder = NewsFinder(
            start_date=self.start_date,
            end_date=self.end_date,
            company=self.company,
            api_key=api_key,
        )

    def run(self):
        """
        runs methods to find, rank and analysis news articles.

        :return: DataFrame with one row per article analysed and columns for key statistics from article analysis.
        """
        logging.info("Chain Run Starting")

        articles, total_articles = self.news_finder.get_articles()

        descriptions = [article["description"] for article in articles]
        sentiments = self.sentiment_analysis.perform_sentiment_analysis(descriptions)

        # prepare output
        filtered_contents = [
            {"source": article["source"]["name"], "publishedAt": article["publishedAt"]}
            for article in articles
        ]
        df = pd.DataFrame(filtered_contents)
        df["sentiments"] = sentiments

        return df, total_articles
