import html
import json
import re
from collections import Counter
from pathlib import Path
from urllib.request import urlopen

import matplotlib
matplotlib.use("Agg")  # Save images without needing a desktop or CODIO.
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import STOPWORDS, WordCloud

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "output"
EMAIL_URL = "https://raw.githubusercontent.com/bendgame/nlpBeginnerProjects/master/emails.csv"
SQUAD_URL = "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json"
STOP_WORDS = set(STOPWORDS) | {"subject", "re", "fw", "fwd", "http", "https", "www"}


def download(url, filename):
    path = DATA / filename
    if not path.exists():
        with urlopen(url, timeout=90) as response:
            content = response.read()
        path.write_bytes(content)
    return path


def clean_text(text):
    text = html.unescape(text).lower()
    text = re.sub(r"<[^>]*>", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    return " ".join(text.split())


def count_words(texts):
    counts = Counter()
    for text in texts:
        counts.update(word for word in clean_text(text).split()
                      if len(word) > 1 and word not in STOP_WORDS)
    if not counts:
        raise ValueError("No words remain after cleaning and stop-word removal.")
    return counts


def make_cloud(counts, color):
    return WordCloud(width=1200, height=800, background_color="white",
                     max_words=120, min_font_size=10, random_state=7,
                     colormap=color, collocations=False).generate_from_frequencies(counts)


def save_cloud(counts, title, name, color="viridis"):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(make_cloud(counts, color), interpolation="bilinear")
    ax.set_title(title, fontsize=18, pad=16)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.png", dpi=160)
    plt.close(fig)


def save_comparison(groups, title, name):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    for ax, (label, counts, color) in zip(axes, groups):
        ax.imshow(make_cloud(counts, color), interpolation="bilinear")
        ax.set_title(label, fontsize=16, pad=12)
        ax.axis("off")
    fig.suptitle(title, fontsize=20)
    fig.text(0.5, 0.025, "Word sizes are relative within each cloud; compare counts in results.txt.",
             ha="center", fontsize=11)
    fig.tight_layout(rect=(0, 0.05, 1, 0.94))
    fig.savefig(OUT / f"{name}.png", dpi=160)
    plt.close(fig)


def describe(name, counts):
    top = ", ".join(f"{word} ({count})" for word, count in counts.most_common(10))
    return f"{name}: {sum(counts.values()):,} retained tokens\nTop 10: {top}"


def main():
    DATA.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    lines = ["TECHNICAL 9 - NATURAL LANGUAGE PROCESSING", "", "VI. EMAIL ACTIVITY"]

    # 1. Import data. 2. Inspect labels, missing records, and duplicates.
    emails = pd.read_csv(download(EMAIL_URL, "emails.csv"))
    emails = emails[["text", "spam"]]
    original_count = len(emails)
    lines.append(f"Original rows: {original_count:,}")
    lines.append(f"Original label counts: {emails['spam'].value_counts().sort_index().to_dict()}")
    emails = emails.dropna(subset=["text", "spam"])
    missing = original_count - len(emails)
    emails["spam"] = pd.to_numeric(emails["spam"], errors="raise").astype(int)
    if not emails["spam"].isin([0, 1]).all():
        raise ValueError("Expected spam labels 0 or 1.")
    duplicates = int(emails.duplicated().sum())
    emails = emails.drop_duplicates().reset_index(drop=True)
    lines.extend([f"Missing records removed: {missing}",
                  f"Duplicate rows removed: {duplicates}",
                  f"Remaining rows: {len(emails):,}",
                  f"Remaining label counts: {emails['spam'].value_counts().sort_index().to_dict()}"])

    # 3. Clean text. 4. Remove stop words. 5. Construct word clouds.
    all_counts = count_words(emails["text"])
    spam_counts = count_words(emails.loc[emails["spam"] == 1, "text"])
    ham_counts = count_words(emails.loc[emails["spam"] == 0, "text"])
    save_cloud(all_counts, "Technical 9 | All emails", "part_vi_all_emails")
    save_comparison([("Spam", spam_counts, "magma"),
                     ("Non-spam", ham_counts, "viridis")],
                    "Technical 9 | Email comparison", "part_vi_email_comparison")
    for label, counts in [("All emails", all_counts), ("Spam", spam_counts), ("Non-spam", ham_counts)]:
        lines.extend(["", describe(label, counts)])

    # VII. Repeat on two explicitly selected articles from SQuAD 1.1 dev.
    squad = json.loads(download(SQUAD_URL, "squad_dev_v1.1.json").read_text(encoding="utf-8"))
    selected = ["Super_Bowl_50", "Warsaw"]
    records = [{"topic": article["title"], "text": paragraph["context"]}
               for article in squad["data"] if article["title"] in selected
               for paragraph in article["paragraphs"]]
    topics = pd.DataFrame(records)
    before = len(topics)
    topics = topics.dropna().drop_duplicates().reset_index(drop=True)
    # Read each context once, rather than repeating it for every associated question.
    groups = []
    lines.extend(["", "VII. SQUAD CHALLENGE", "Subset: Super Bowl 50 and Warsaw, SQuAD 1.1 development split.",
                  f"Original paragraphs: {before}", f"Unique paragraphs: {len(topics)}"])
    for topic, color in zip(selected, ["plasma", "viridis"]):
        subset = topics.loc[topics["topic"] == topic, "text"]
        counts = count_words(subset)
        label = topic.replace("_", " ")
        groups.append((label, counts, color))
        lines.extend(["", f"{label}: {len(subset)} paragraphs", describe(label, counts)])
        save_cloud(counts, f"Technical 9 | {label}", f"part_vii_{topic.lower()}", color)
    save_comparison(groups, "Technical 9 | SQuAD topic comparison", "part_vii_comparison")
    results = "\n".join(lines) + "\n"
    (OUT / "results.txt").write_text(results, encoding="utf-8")
    print(results)
    print(f"Saved figures and results to {OUT}")


if __name__ == "__main__":
    main()
