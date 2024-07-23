import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import requests
import re

# Load stop words
stop_words = set(stopwords.words('english')) 
for file in ['Test Assignment/StopWords/StopWords_Auditor.txt',                 # *********Replace this
             'Test Assignment/StopWords/StopWords_Currencies.txt',              # *********Replace this
             'Test Assignment/StopWords/StopWords_DatesandNumbers.txt',         # *********Replace this
             'Test Assignment/StopWords/StopWords_Generic.txt',                 # *********Replace this
             'Test Assignment/StopWords/StopWords_GenericLong.txt',             # *********Replace this
             'Test Assignment/StopWords/StopWords_Geographic.txt',              # *********Replace this
             'Test Assignment/StopWords/StopWords_Names.txt']:                  # *********Replace this
    with open(file, 'r') as f:
        stop_words.update(f.read().split())

# Load positive and negative words
positive_words = set()
negative_words = set()
with open('Test Assignment/MasterDictionary/positive-words.txt', 'r') as f:   # *********Replace this
    positive_words.update(f.read().split())
with open('Test Assignment/MasterDictionary/negative-words.txt', 'r') as f:    # *********Replace this
    negative_words.update(f.read().split())

# Remove stop words from positive and negative words lists
positive_words = positive_words - stop_words
negative_words = negative_words - stop_words



def append_xlsx(file_path, analysis_results, url):
    # Load the existing Excel file
    df = pd.read_excel(file_path)

    # Find the row corresponding to the URL
    row_index = df[df['URL'] == url].index

    # If the URL is found, update the row with the analysis results
    if not row_index.empty:
        for key, value in analysis_results.items():
            df.at[row_index[0], key] = value  # Update the specific row
    else:
        # If the URL is not found, create a new row
        new_row = {'URL': url}
        new_row.update(analysis_results)
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)

    # Save the updated DataFrame back to the Excel file
    df.to_excel(file_path, index=False)

def extract_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Try to find the main heading first
    main_heading = soup.find('h1')

    article_containers = soup.find_all(['article', 'div', 'section'])

    # Choose the most likely article container (heuristic approach)
    article_container = max(article_containers, key=lambda x: len(x.text))

    # Extract article title
    title = article_container.find('h1').text.strip() if article_container.find('h1') else None

    # Extract article text
    article_text = ' '.join(p.text.strip() for p in article_container.find_all('p'))

    
    unwanted_patterns = [
        r'Summarized:.*',  
        r'This project was done by.*',  
        r'Here are my contact details:.*',  
        r'Firm Name:.*',  
        r'Firm Website:.*',  
        r'Firm Address:.*',  
        r'Email:.*',  
        r'Skype:.*',  
        r'WhatsApp:.*',  
        r'Telegram:.*',  
        r'Contact us:.*',  
        r'© All Right Reserved,.*'  
    ]

    for pattern in unwanted_patterns:
        article_text = re.sub(pattern, '', article_text, flags=re.DOTALL)

    # Remove any extra whitespace
    article_text = re.sub(r'\s+', ' ', article_text).strip()

    return title, article_text

def save_to_file(title, text, filename='article.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(title + '\n\n')
        f.write(text)
    print(title, text)

def calculate_syllable_count(word):
    word = word.lower()
    count = 0
    vowels = "aeiou"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("es") or word.endswith("ed"):
        count -= 1
    return max(1, count)

def count_personal_pronouns(text):
    pronouns = ['I', 'we', 'my', 'ours', 'us']
    pronoun_count = 0
    for pronoun in pronouns:
        pronoun_count += len(re.findall(r'\b' + pronoun + r'\b', text, re.IGNORECASE))
    return pronoun_count

def analyze_text_content(text, url):
    # Tokenization
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    # Calculate sentiment scores
    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)

    # Calculate readability metrics
    avg_sentence_length = sum(len(sentence.split()) for sentence in sentences) / len(sentences)
    complex_words = [word for word in words if calculate_syllable_count(word) > 2]
    percentage_complex_words = len(complex_words) / len(words) * 100
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = len(words) / len(sentences)
    complex_word_count = len(complex_words)
    word_count = len(words)
    syllable_per_word = sum(calculate_syllable_count(word) for word in words) / len(words)
    personal_pronouns = count_personal_pronouns(text)
    avg_word_length = sum(len(word) for word in words) / len(words)

    # Create a dictionary to store results
    results = {
        'POSITIVE SCORE': positive_score,
        'NEGATIVE SCORE': negative_score,
        'POLARITY SCORE': polarity_score,
        'SUBJECTIVITY SCORE': subjectivity_score,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_words_per_sentence,
        'COMPLEX WORD COUNT': complex_word_count,
        'WORD COUNT': word_count,
        'SYLLABLE PER WORD': syllable_per_word,
        'PERSONAL PRONOUNS': personal_pronouns,
        'AVG WORD LENGTH': avg_word_length
    }
    append_xlsx('Output Data Structure.xlsx', results, url)                  # *********Replace this

def analyze_text_from_file(file_path, url):
    """Reads text from a file and performs analysis."""
    with open('article.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    
    analyze_text_content(text, url)

def loopURLL(url):
    title, text = extract_article(url)

    if title and text:
        save_to_file(title, text)
        file_path = 'article.txt'
        analyze_text_from_file(file_path, url)
    else:
        print("Failed to extract article content.")

def process_urls_from_excel(excel_file):
    """Processes URLs from an Excel file using the loopURLL function."""

    df = pd.read_excel(excel_file)
    urls = df['URL'].tolist()

    for url in urls:
        loopURLL(url)

process_urls_from_excel('Input.xlsx')                                   # *********Replace this 
