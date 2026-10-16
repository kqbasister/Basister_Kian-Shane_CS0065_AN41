# Intelligent Tutoring System Using Case Based Reasoning

This project is a Python implementation of an Intelligent Tutoring System (ITS) for Technical Assessment 3. It uses Case-Based Reasoning (CBR) to recommend personalized mathematics support from successful past student cases.

The included demonstration considers a Grade 8 student who repeatedly uses the wrong inverse operation when solving linear equations. The program retrieves the most similar prior case, adapts its learning plan, reviews a follow-up result, and saves the new experience to the case base.

## Features

- Stores five initial fictional student cases in a JSON case base.
- Ranks successful past cases using a weighted similarity score.
- Matches the topic, error pattern, grade level, and error frequency.
- Generates adapted feedback, guided support, a practice count, and a worked example when appropriate.
- Reviews a follow-up quiz result and adds support when the result is below 80%.
- Retains the newly solved case without adding duplicate records.
- Provides an interactive mode for entering a different student profile.

## Case Based Reasoning Cycle

1. **Retrieve** - Find and rank successful cases that are similar to the new student profile.
2. **Reuse and adapt** - Reuse the most relevant strategy and tailor it to the current student.
3. **Revise** - Review the follow-up quiz result and strengthen the support plan if needed.
4. **Retain** - Save the outcome as a new case so it can help with future decisions.

## Similarity Method

The program calculates a weighted similarity score from 0% to 100%:

```text
score = 100 x (0.30 x topic + 0.45 x errors + 0.15 x grade + 0.10 x frequency)
```

Error matching uses Jaccard similarity: shared error types divided by all distinct error types in the two cases. Error patterns have the highest weight because they are the strongest indicator of the support a student needs.

## Requirements

- Python 3.10 or later
- No third-party packages

## Run the Demonstration

From this project folder, run:

```bash
python main.py
```

The demonstration loads five seed cases, retrieves Case `C01` at 95% similarity, adapts the plan, uses a clearly labelled simulated follow-up score of 4/5, and saves the result as `C06` in `case_base.json`.

## Interactive Mode

Run the following command to enter a new student profile:

```bash
python main.py --interactive
```

The program asks for the mathematics topic, main error, grade, error frequency, description, and follow-up quiz score. Enter `-1` for the score when the follow-up quiz has not yet been taken; the saved case will be marked as pending.

To experiment without changing the supplied case base, use a different JSON filename:

```bash
python main.py --data fresh_cases.json
```

## Files

| File | Purpose |
| --- | --- |
| `main.py` | Main CBR program and interactive interface. |
| `case_base.json` | Initial set of five fictional student cases. The program updates this file when it retains a new case. |
| `test_main.py` | Automated behavior checks for retrieval, adaptation, revision, persistence, and validation. |
| `documentation.html` | Short project documentation with a program-execution screenshot and pair reflection. |
| `sample_output.txt` | Text copy of the demonstration output. |

## Run Tests

```bash
python -m unittest -v
```

## Notes

All seed cases and demonstration outcomes are fictional examples for classroom use. The program uses teacher-labelled error patterns; it does not automatically diagnose a student's handwritten or typed algebra work.
