from pydantic import BaseModel
from typing import List
from transformers import pipeline


class SentimentAnalysis(BaseModel):
    _sentiment_pipeline: pipeline

    def __init__(self):
        super().__init__()
        self._sentiment_pipeline = pipeline("sentiment-analysis")

    def perform_sentiment_analysis(self, articles: List[str]) -> List[float]:
        """
        Performs sentiment analysis on a provided list of articles and returns scores in a list of the same length.

        :param articles: List of news articles
        :return: List of sentiment scores for articles (positive: +score, negative: -score)
        """
        sentiment_results = []

        for article in articles:
            # Perform sentiment analysis
            try:
                result = self._sentiment_pipeline(article)[0]

                # Extract score: positive scores are kept positive, negative are converted to negative
                score = result["score"] if result["label"] == "POSITIVE" else -result["score"]
                sentiment_results.append(score)
            except Exception as e:
                sentiment_results.append(None)

                print(f"Error {e} during sentiment pipeline.")
                print(f"Article: {article}")

        return sentiment_results

