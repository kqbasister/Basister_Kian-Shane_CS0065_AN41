# Technical Assessment 4: Classroom Comfort Adviser

**CS0065 - Intelligent Systems**  
**Topic:** Implementing Knowledge Representation, Rule-Based Reasoning (RBR), and Case-Based Reasoning (CBR)

| Student | Section |
| --- | --- |
| Calingasan, Dwayne Giusseppe P. | AN41 |
| Basister, Kian Shane | AN41 |

**Professor:** Ms. Tan

## Overview

This Python console application recommends actions to improve classroom comfort based on climate, weather, and room conditions. It demonstrates two reasoning approaches using the same current observations:

- **Rule-Based Reasoning (RBR):** Checks explicit IF-THEN rules and returns every applicable action.
- **Case-Based Reasoning (CBR):** Finds a similar past situation, reuses its solution, allows a revision, and retains the resulting case for the current run.

The program displays its input facts, reasoning process, and recommendations. It is an educational adviser that prints actions; it does not control physical appliances.

## Project Files

| File | Description |
| --- | --- |
| `TA4_Basister.py` | Complete implementation of the knowledge base, RBR engine, and CBR cycle. |
| `TA4_Calingasan-Basister.pdf` | Assessment instructions, comparative reflection, source code, and output screenshots. |
| `README.md` | Project overview, execution instructions, and implementation notes. |

## Requirements

- Python 3 with support for f-strings (Python 3.6 or later).
- A terminal or an editor capable of running Python scripts.

The program uses only Python's standard library (`argparse` and `copy`). No third-party packages or installation commands are required.

## How to Run

Open a terminal in this folder and choose one of the following modes.

### Interactive mode

```sh
python TA4_Basister.py
```

After displaying the RBR actions and retrieving a CBR solution, the program prompts:

```text
REVISE: new solution, or Enter to keep:
```

Enter a complete replacement solution, or press **Enter** to keep the retrieved solution. For the default classroom facts, an example revision is:

```text
Close the windows. Turn on the lights. Turn on the aircon.
```

### Demo mode

```sh
python TA4_Basister.py --demo
```

This runs without a prompt and appends `Turn on the aircon.` to the retrieved solution as a scripted revision. It provides a reproducible demonstration of the full CBR cycle.

On Windows, if `python` is unavailable but the Python launcher is installed, use `py` instead. To see the available command-line option, run:

```sh
python TA4_Basister.py --help
```

## Part 1: Knowledge Representation

The `FACTS` dictionary stores six observations in three categories, meeting the assessment's requirement of at least five facts and three categories.

| Category | Fact | Default value |
| --- | --- | --- |
| `climate` | `temperature` | `"hot"` |
| `climate` | `humidity` | `"high"` |
| `weather` | `is_raining` | `True` |
| `weather` | `is_daylight` | `False` |
| `room` | `is_occupied` | `True` |
| `room` | `windows_open` | `True` |

At startup, `main()` creates independent copies of `FACTS` and `CASE_BASE`. The copied facts serve as working memory, while the copied case base holds past experiences and the newly retained case.

## Part 2: Rule-Based Reasoning

Three functions implement the IF-THEN rules:

| Rule | Condition | Inferred action |
| --- | --- | --- |
| `rule_hot` | Temperature is `"hot"` and the room is occupied. | Turn on the aircon. |
| `rule_rain` | It is raining and the windows are open. | Close the windows. |
| `rule_dark` | It is not daylight and the room is occupied. | Turn on the lights. |

The `RULES` tuple holds these functions. The `infer()` function checks each one, prints `MATCH` or `NO MATCH`, and collects all matching actions. It does not stop after the first match or modify the facts.

All three rules match the default observations:

```text
Rule-Based Reasoning Actions:
- Turn on the aircon.
- Close the windows.
- Turn on the lights.
```

Humidity is represented in the knowledge base and used in CBR similarity matching, but it is not a condition in the current RBR rules.

## Part 3: Case-Based Reasoning

### Initial case base

Each case contains an `id`, a nested `problem` dictionary with six features, and a `solution` string.

| Case | Past situation | Stored solution |
| --- | --- | --- |
| C1 | Hot, high humidity, no rain, daylight, occupied room, closed windows. | Turn on the aircon. |
| C2 | Warm, high humidity, rain, no daylight, occupied room, open windows. | Close the windows. Turn on the lights. |
| C3 | Cool, normal humidity, no rain, daylight, unoccupied room, closed windows. | Keep the aircon and lights off. |

### The 4R cycle

1. **Retrieve:** `retrieve()` compares the current problem with every stored case and selects the highest similarity score.
2. **Reuse:** `reuse()` returns the selected case's existing solution.
3. **Revise:** `revise()` uses the user's replacement text, or keeps the original solution if the response is empty or whitespace. Demo mode supplies a scripted replacement.
4. **Retain:** `retain()` appends a new case containing a deep copy of the current problem and the final solution.

### Similarity calculation

`flatten()` converts nested facts into `(category, feature)` keys so that each feature retains its category. Similarity uses equally weighted, exact-value matches:

```text
Similarity = Number of matching query features / Total number of query features
```

For the default six facts:

| Case | Matching features | Similarity |
| --- | --- | --- |
| C1 | 3 of 6 | 50.00% |
| C2 | 5 of 6 | 83.33% |
| C3 | 0 of 6 | 0.00% |

C2 is selected because only its temperature (`"warm"`) differs from the current temperature (`"hot"`). If cases tie, the earliest case in the list wins. An empty query or an empty case base raises a `ValueError`.

After revision, the current problem is retained as C4. The program retrieves the same problem again to demonstrate that C4 now matches all six features, giving a similarity of **100.00%**. This score measures feature agreement, not whether the retained solution is correct.

### Example demo output (excerpt)

```text
CBR PROCESS: RETRIEVE
  C1: similarity = 50.00%
  C2: similarity = 83.33%
  C3: similarity = 0.00%
Selected case: C2 (83.33%)
REUSE: Close the windows. Turn on the lights.
REVISE (demo input): Close the windows. Turn on the lights. Turn on the aircon.
Final CBR solution: Close the windows. Turn on the lights. Turn on the aircon.
RETAIN: added C4; case count = 4
Retention is in memory for this run; no file is written.

Verification: retrieve the same problem after retention
  C1: similarity = 50.00%
  C2: similarity = 83.33%
  C3: similarity = 0.00%
  C4: similarity = 100.00%
Selected case: C4 (100.00%)
```

The PDF also shows interactive runs where the retrieved solution is either kept unchanged or manually revised to include the aircon recommendation.

## Part 4: Comparative Reflection

RBR was easier to implement in this activity because each condition maps directly to an action using a Python `if` statement. CBR requires additional steps to compare cases, select a solution, revise it, and retain the new experience.

CBR offers flexibility for less structured problems by adapting previous solutions. Adding relevant cases can help with changing situations, although older cases may need review. RBR remains useful when decision rules are stable and only the input observations change. The report identifies appliance control and troubleshooting as RBR applications, and help-desk support and equipment diagnosis as CBR applications.

In this example, RBR immediately recommends all three actions. CBR initially reuses C2's window and lighting advice; adding the aircon action requires manual revision or the scripted demo revision.

## Customization and Limitations

- Edit `FACTS` to try different classroom conditions. Preserve the category and feature names expected by the rules.
- Edit `CASE_BASE` to change the stored experiences, or add a rule function and include it in `RULES` to extend RBR.
- The interactive prompt changes only the CBR solution; classroom observations are configured in the source code.
- Retained cases exist **only in memory during the current run**. Restarting the script restores the original three cases; no file or database is updated.
- Similarity uses exact matches with equal weights. It does not measure how close values such as `"warm"` and `"hot"` are.
- The program selects the best available case even when its similarity is low; there is no minimum acceptance threshold.
- Revised solutions are stored as text without checking their correctness. The demo's aircon addition is fixed and should be reviewed if the input facts are changed.
