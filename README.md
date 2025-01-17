# News Analysis Project 

This is a project that uses NewsAPI to retrieve articles from over ?500?
news sources and perform sentiment analysis on the article descriptions.

This project includes a frontend that allows a user to input a company
and ticker of their choice and see some visualisations of how positively
news articles have been reporting on that company for up to the past month
along with the stock price of that ticker.


# Installation Instructions for `NewsAnalysis`

Follow these steps to install and run the `NewsAnalysis` project.

## Prerequisites
Ensure that Poetry is installed on your system. If not, follow the [Poetry installation guide](https://python-poetry.org/docs/#installation).

## Steps

### 1. Clone the Repository
Clone the GitHub repository to your local machine:

```bash
git clone https://github.com/DanielBibby/NewsAnalysis.git
cd NewsAnalysis
```

### 2. Generate a free API key and add it to .env
You can get a free API key in 30 seconds [here](https://newsapi.org)
```bash
echo 'NEWS_API_KEY="YOUR_API_KEY_HERE" > .env
```


### 3. Install dependencies and activate the virtual environment
```bash
poetry install
poetry shell
```

### 4. Run the Application
```bash
poetry run streamlit run app.py
```




