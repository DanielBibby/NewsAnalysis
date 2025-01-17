import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def create_dashboard(stock_data, ticker, sentiments_df):
    sentiments_df["date"] = pd.to_datetime(sentiments_df["publishedAt"]).dt.date

    # Add a column for sentiment polarity
    sentiments_df["sentiment_type"] = sentiments_df["sentiments"].apply(
        lambda x: "positive" if x > 0 else "negative"
    )

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    # Plot 1: Number of rows for each day split by sentiment
    daily_counts = (
        sentiments_df.groupby(["date", "sentiment_type"]).size().unstack(fill_value=0)
    )
    daily_counts.plot(kind="line", ax=axs[0, 0])
    axs[0, 0].set_title("Number of Articles Per Day by Sentiment")
    axs[0, 0].set_xlabel("Date")
    axs[0, 0].set_ylabel("Number of Articles")
    axs[0, 0].legend(title="Sentiment")
    axs[0, 0].tick_params(axis="x", rotation=30)

    # Plot 2 - Number of positive / negative articles
    daily_mean_sentiments = (
        sentiments_df.groupby(["date", "sentiment_type"])["sentiments"]
        .mean()
        .unstack(fill_value=0)
    )
    daily_mean_sentiments.plot(kind="bar", ax=axs[0, 1])
    axs[0, 1].set_title("Mean Sentiment Score Per Day by Sentiment")
    axs[0, 1].set_xlabel("Date")
    axs[0, 1].set_ylabel("Mean Sentiment Score")
    axs[0, 1].legend(title="Sentiment")
    axs[0, 1].tick_params(axis="x", rotation=30)

    # Plot 3 - Pie chart of sentiment sources
    source_counts = sentiments_df["source"].value_counts()
    axs[1, 0].pie(
        source_counts,
        labels=source_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 8},
    )
    axs[1, 0].set_title("Article Sources Distribution")

    # Plot 4 - Stock Price Plot
    axs[1, 1].plot(
        stock_data.index, stock_data["Close"], label="Close Price", color="blue"
    )

    # Use MaxNLocator to avoid overlapping xticks
    axs[1, 1].xaxis.set_major_locator(MaxNLocator(nbins=6))  # Limit the number of ticks
    axs[1, 1].set_title(f"Closing Prices for {ticker}")
    axs[1, 1].set_xlabel("Date")
    axs[1, 1].set_ylabel("Price")
    axs[1, 1].legend()
    axs[1, 1].grid(True)
    axs[1, 1].tick_params(axis="x", rotation=30)

    # Adjust layout to prevent overlap
    plt.tight_layout()

    return fig
