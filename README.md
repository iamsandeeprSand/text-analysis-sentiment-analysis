Here is a `README.md` file for your project:

```markdown
# Text Analysis and Sentiment Analysis Project

This project involves extracting, analyzing, and processing articles from provided URLs. It performs sentiment analysis, readability metrics calculation, and updates the results to an Excel file.

## Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
The project performs the following tasks:
1. Extracts the main content of articles from given URLs.
2. Cleans and preprocesses the text.
3. Calculates various sentiment and readability metrics.
4. Updates the results into an existing Excel file.

### Sentiment Analysis Metrics
- Positive Score
- Negative Score
- Polarity Score
- Subjectivity Score

### Readability Metrics
- Average Sentence Length
- Percentage of Complex Words
- Fog Index
- Average Number of Words per Sentence
- Complex Word Count
- Word Count
- Syllable per Word
- Personal Pronouns Count
- Average Word Length

## Installation
To get started with this project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/iamsandeeprSand/text-analysis-sentiment-analysis.git
cd text-analysis-sentiment-analysis
pip install -r requirements.txt
```

### Dependencies
- pandas
- BeautifulSoup4
- nltk
- requests
- openpyxl

Ensure that you have the `nltk` data files:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Usage
1. **Prepare Input Files**:
   - `Input.xlsx`: Excel file containing URLs of articles to be analyzed.
   - Stopwords files: Update the paths in the script to the actual locations of your stopwords files.
   - Sentiment words files: Ensure paths to positive and negative words files are correct.

2. **Run the Script**:
   ```bash
   python main.py
   ```

   The script will:
   - Extract and clean the article content.
   - Perform sentiment and readability analysis.
   - Update the results in `Output Data Structure.xlsx`.

## Project Structure
```
text-analysis-sentiment-analysis/
│
├── Test Assignment/
│   ├── StopWords/
│   │   ├── StopWords_Auditor.txt
│   │   ├── StopWords_Currencies.txt
│   │   ├── StopWords_DatesandNumbers.txt
│   │   ├── StopWords_Generic.txt
│   │   ├── StopWords_GenericLong.txt
│   │   ├── StopWords_Geographic.txt
│   │   └── StopWords_Names.txt
│   └── MasterDictionary/
│       ├── positive-words.txt
│       └── negative-words.txt
│
├── Input.xlsx
├── Output Data Structure.xlsx
├── article.txt
├── main.py
├── requirements.txt
└── README.md
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes.
