# Sentiment Analysis

Python programs for CS054 Intelligent Systems, Technical 5. The main activity uses TextBlob to analyze 10 sentences. The challenge counts happy and sad words using public word lists.

## Project files

| File | Purpose |
| --- | --- |
| `laboratory_technical_5.py` | Analyzes 10 sentences and summarizes their sentiments. |
| `challenge.py` | Counts happy and sad words and determines the sentence's tone. |
| `requirements.txt` | Specifies the TextBlob dependency. |
| `data/positive-words.txt` | Positive words used by the challenge. |
| `data/negative-words.txt` | Negative words used by the challenge. |
| `data/README.txt` | Original dataset attribution and source information. |
| `output/` | Completed activity sheet, sample output, and code screenshots. |

## Setup

Install Python 3, then open a terminal in this project folder and install the dependency:

```powershell
python -m pip install -r requirements.txt
```

The challenge uses only Python's standard library. Keep the `data` folder beside `challenge.py` so it can load both word lists.

## Run the main activity

```powershell
python laboratory_technical_5.py
```

Enter one sentence at each prompt. The program accepts 10 non-empty sentences, displays each sentence's polarity and sentiment, and prints the totals.

| Polarity | Sentiment |
| --- | --- |
| Less than 0 | Negative |
| Equal to 0 | Neutral |
| Greater than 0 | Positive |

Blank input is rejected and does not count toward the 10 sentences.

### Sample sentences

Enter these sentences one at a time:

1. I love this wonderful day.
2. This is a terrible experience.
3. The book is on the table.
4. The service was excellent.
5. I hate this awful weather.
6. The meeting starts at noon.
7. This is a beautiful place.
8. The food was bad.
9. She has a blue notebook.
10. I am happy with the results.

Expected summary with the specified TextBlob version:

```text
SUMMARY (10 sentences)
Positive: 4
Neutral: 3
Negative: 3
```

## Run the challenge

```powershell
python challenge.py
```

Enter one sentence. The program uses two functions:

- `number_happy(sentence)` counts occurrences of words in the positive list.
- `number_sad(sentence)` counts occurrences of words in the negative list.

More happy words produces **Positive (happy)**. More sad words produces **Negative (sad)**. Equal counts produce **Neutral**, including when neither list has a matching word.

Example:

```text
Enter a sentence: Happy, HAPPY! sad.
Happy words: 2
Sad words: 1
Analysis: Positive (happy)
```

Matching ignores capitalization and surrounding punctuation. Repeated words count each time they appear. Hyphenated words and contractions remain whole tokens.

This simple counting method does not interpret context, sarcasm, or negation. For example, `not happy` still contains one happy word.

## Use the existing Windows virtual environment

If you are working in the original workspace, its `.venv` already has TextBlob installed. Run:

```powershell
.\.venv\Scripts\python.exe laboratory_technical_5.py
.\.venv\Scripts\python.exe challenge.py
```

If `.venv` is absent, use the setup instructions above.

## Dataset and references

The challenge uses the **Hu and Liu Opinion Lexicon**, distributed through NLTK, with separate lists of 2,006 positive and 4,783 negative entries. The original dataset headers and attribution are retained in `data/`.

Minqing Hu and Bing Liu. *Mining and Summarizing Customer Reviews.* Proceedings of ACM SIGKDD, 2004.

- [Original Opinion Lexicon source](https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html)
- [NLTK dataset download](https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/opinion_lexicon.zip)
- [TextBlob sentiment analysis documentation](https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis)

The programs run locally; CODIO is not required.
