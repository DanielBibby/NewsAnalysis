import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from pandas import DataFrame


def create_dashboard(stock_data, ticker, sentiments_df):
    sentiments_df["date"] = pd.to_datetime(sentiments_df["publishedAt"]).dt.date

    # Add a column for sentiment polarity
    sentiments_df["sentiment_type"] = sentiments_df["sentiments"].apply(
        lambda x: "positive" if x > 0 else "negative"
    )

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    fig.set_facecolor("#ece0cb")

    # Plot 1: Number of rows for each day split by sentiment (Bar Plot)
    daily_counts = (
        sentiments_df.groupby(["date", "sentiment_type"]).size().unstack(fill_value=0)
    )
    daily_counts.plot(
        kind="bar",
        ax=axs[0, 0],
        color={"positive": "#136207", "negative": "#990000"},
    )
    axs[0, 0].set_title("Number of Articles Per Day by Sentiment")
    axs[0, 0].set_xlabel("Date")
    axs[0, 0].set_ylabel("Number of Articles")
    axs[0, 0].legend(title="Sentiment")
    axs[0, 0].tick_params(axis="x", rotation=30)

    # Plot 2 - Stock Price Plot
    if isinstance(stock_data, DataFrame):
        axs[0, 1].plot(
            stock_data.index, stock_data["Close"], label="Close Price", color="blue"
        )

        # Use MaxNLocator to avoid overlapping xticks
        axs[0, 1].xaxis.set_major_locator(
            MaxNLocator(nbins=6)
        )  # Limit the number of ticks
        axs[0, 1].set_title(f"Closing Prices for {ticker}")
        axs[0, 1].set_xlabel("Date")
        axs[0, 1].set_ylabel("Price")
        axs[0, 1].legend()
        axs[0, 1].grid(True)
        axs[0, 1].tick_params(axis="x", rotation=30)

    else:
        axs[
            0,
            1,
        ].axis("off")

    # Plot 3 - Pie chart of sentiment sources
    source_counts = sentiments_df["source"].value_counts()
    total_articles = source_counts.sum()
    threshold = 0.05 * total_articles  # Calculate the 5% threshold

    # Filter sources to include only those with 5% or more
    filtered_sources = source_counts[source_counts >= threshold]
    other_sources_count = total_articles - filtered_sources.sum()

    # Add an "Other" category for remaining sources
    if other_sources_count > 0:
        filtered_sources["Other"] = other_sources_count

    # Create the pie chart
    axs[1, 0].pie(
        filtered_sources,
        labels=filtered_sources.index,
        autopct=lambda p: f"{p:.1f}%" if p >= 5 else "",
        startangle=90,
        textprops={"fontsize": 8},
    )

    # Set the title and include the count of unique publishers
    unique_publishers = len(source_counts)
    axs[1, 0].set_title(
        f"Article Sources Distribution\n({unique_publishers} unique publishers)"
    )

    # Plot 4 - Table of news sources
    top_sources = source_counts.head(10)  # Select the top 10 sources
    table_data = [
        [source, count] for source, count in zip(top_sources.index, top_sources.values)
    ]
    table_columns = ["Source", "Number of Articles"]

    # Add the table to axs[1, 1]
    axs[1, 1].axis("off")  # Turn off the axes for the table
    table = axs[1, 1].table(
        cellText=table_data,
        colLabels=table_columns,
        loc="center",
        cellLoc="center",
        colLoc="center",
    )

    # Adjust the font size for better readability
    # table.auto_set_font_size(False)
    # table.set_fontsize(11)
    table.auto_set_column_width([0, 1])  # Adjust column widths

    # Adjust layout to prevent overlap
    plt.tight_layout()

    return fig
