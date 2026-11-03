# Technical 9: Natural Language Processing

This CS0054 Intelligent Systems activity uses Python to clean text, count word frequencies, and generate word clouds. It includes an email analysis for Part VI and a comparison of two SQuAD article topics for Part VII.

The project runs locally without CODIO. It saves PNG images and a text summary for use in the activity document.

## Activities

### Part VI: Email analysis

- Load the email dataset with pandas.
- Check missing values and remove duplicate records.
- Clean the text and remove stop words.
- Generate a word cloud for all emails and a comparison of spam and non-spam emails.
- Record the dataset counts and ten most frequent words for each group.

The spam labels come from the dataset: `1` means spam and `0` means non-spam. The program visualizes those groups; it does not train a spam classifier.

### Part VII: SQuAD challenge

Apply the same procedure to context paragraphs from the **Super Bowl 50** and **Warsaw** articles in the SQuAD 1.1 development dataset. Each paragraph is counted once, regardless of how many questions refer to it. The output compares the vocabulary of the two topics.

## Setup and execution

Install Python and run the following commands in PowerShell from the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe technical9.py
```

If the virtual environment is already set up, run only:

```powershell
.\.venv\Scripts\python.exe technical9.py
```

The dependencies are pandas, Matplotlib, and WordCloud, with versions recorded in `requirements.txt`. An internet connection is needed to install dependencies and download any missing datasets. Later runs can use the cached files in `data/` without downloading them again.

The script prints its results and saves all figures in `output/`. It does not open plot windows. Running it again replaces the generated images and `results.txt`. Input and output paths are resolved relative to the script's location.



## Text processing

The program decodes HTML entities, converts text to lowercase, removes HTML tags and URLs, and replaces characters other than English letters and whitespace with spaces. It then removes one-character tokens and words in the WordCloud stop-word list, extended with `subject`, `re`, `fw`, `fwd`, `http`, `https`, and `www`.

Word clouds are generated from explicit token counts. Each cloud displays up to 120 words and uses a fixed random seed of `7`. Exact appearance can still vary with fonts and library versions.

## Recorded results

These counts were obtained from the supplied cached datasets:

| Email measure | Count |
| --- | ---: |
| Original records | 5,728 |
| Missing records removed | 0 |
| Duplicate records removed | 33 |
| Remaining records | 5,695 |
| Remaining spam records | 1,368 |
| Remaining non-spam records | 4,327 |

| SQuAD topic | Unique paragraphs | Retained tokens | Most frequent word |
| --- | ---: | ---: | --- |
| Super Bowl 50 | 54 | 3,408 | bowl (113) |
| Warsaw | 49 | 3,465 | warsaw (150) |

The combined email cloud is dominated by `enron`, `ect`, and `vince`. The selected SQuAD passages emphasize sports vocabulary for Super Bowl 50 and city-related vocabulary for Warsaw. Full counts are saved in `output/results.txt`.

## Interpretation and limitations

- Font sizes are scaled independently within each cloud. Use the recorded counts for numerical comparisons between clouds.
- Word frequency does not establish sentiment, importance, or classification accuracy.
- Email names, headers, signatures, and quoted replies can dominate the email results.
- Cleaning can leave fragments such as `th` from ordinal numbers. Related forms such as `yard` and `yards` are counted separately, and phrases such as `Super Bowl` are split into individual words.
- The challenge covers only two selected SQuAD articles. Its findings do not represent the entire dataset.


## Dataset sources

- **Emails:** [bendgame/nlpBeginnerProjects](https://github.com/bendgame/nlpBeginnerProjects), the repository referenced by the activity handout. The script downloads its `emails.csv` file.
- **SQuAD:** [Stanford Question Answering Dataset](https://rajpurkar.github.io/SQuAD-explorer/), specifically the [SQuAD 1.1 development JSON](https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json). The dataset is distributed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); the challenge figures derive from its context passages.

The handout's Analytics India Magazine dataset-list page was not readable during preparation. A [matching ten-dataset list on Kaggle](https://www.kaggle.com/getting-started/330370) includes SQuAD. The dataset itself was downloaded directly from the Stanford project website.
