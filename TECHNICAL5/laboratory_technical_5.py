from textblob import TextBlob


def main():
    counts = {"Positive": 0, "Neutral": 0, "Negative": 0}

    for number in range(1, 11):
        sentence = input(f"Enter sentence {number}/10: ").strip()
        while not sentence:
            print("Please enter a non-empty sentence.")
            sentence = input(f"Enter sentence {number}/10: ").strip()

        s = TextBlob(sentence)
        p = s.sentiment.polarity

        if p < 0:
            sentiment = "Negative"
        elif p == 0:
            sentiment = "Neutral"
        else:
            sentiment = "Positive"

        counts[sentiment] += 1
        print(f"{sentiment} (polarity: {p:.3f})")

    print("\nSUMMARY (10 sentences)")
    for sentiment, count in counts.items():
        print(f"{sentiment}: {count}")


if __name__ == "__main__":
    main()
