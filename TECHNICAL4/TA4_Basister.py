import argparse
from copy import deepcopy


# PART 1: Six facts grouped into three explicit categories.
FACTS = {
    "climate": {"temperature": "hot", "humidity": "high"},
    "weather": {"is_raining": True, "is_daylight": False},
    "room": {"is_occupied": True, "windows_open": True},
}

# Three illustrative past situations, each with features and a solution.
CASE_BASE = [
    {
        "id": "C1",
        "problem": {
            "climate": {"temperature": "hot", "humidity": "high"},
            "weather": {"is_raining": False, "is_daylight": True},
            "room": {"is_occupied": True, "windows_open": False},
        },
        "solution": "Turn on the aircon.",
    },
    {
        "id": "C2",
        "problem": {
            "climate": {"temperature": "warm", "humidity": "high"},
            "weather": {"is_raining": True, "is_daylight": False},
            "room": {"is_occupied": True, "windows_open": True},
        },
        "solution": "Close the windows. Turn on the lights.",
    },
    {
        "id": "C3",
        "problem": {
            "climate": {"temperature": "cool", "humidity": "normal"},
            "weather": {"is_raining": False, "is_daylight": True},
            "room": {"is_occupied": False, "windows_open": False},
        },
        "solution": "Keep the aircon and lights off.",
    },
]


# PART 2: Each function is one explicit IF-THEN rule.
def rule_hot(facts):
    if facts["climate"]["temperature"] == "hot" and facts["room"]["is_occupied"]:
        return "Turn on the aircon."


def rule_rain(facts):
    if facts["weather"]["is_raining"] and facts["room"]["windows_open"]:
        return "Close the windows."


def rule_dark(facts):
    if not facts["weather"]["is_daylight"] and facts["room"]["is_occupied"]:
        return "Turn on the lights."


RULES = (rule_hot, rule_rain, rule_dark)


def infer(facts):
    """Check EVERY rule against working memory; return all actions."""
    actions = []
    for rule in RULES:
        action = rule(facts)
        print(f"  {rule.__name__}: {'MATCH' if action else 'NO MATCH'}")
        if action is not None:
            actions.append(action)
    return actions


# PART 3: Retrieve, reuse, revise, and retain.
def flatten(facts):
    """Use category/feature pairs to preserve the knowledge structure."""
    return {(category, key): value
            for category, values in facts.items()
            for key, value in values.items()}


def similarity(problem, past_problem):
    """Equal-weight exact matches / number of features in the query."""
    query, past = flatten(problem), flatten(past_problem)
    if not query:
        raise ValueError("The new problem must contain at least one fact.")
    matches = sum(key in past and value == past[key]
                  for key, value in query.items())
    return matches / len(query)


def retrieve(problem, case_base):
    """Return the best case; the earliest case wins a similarity tie."""
    if not case_base:
        raise ValueError("The case base must not be empty.")
    scored = [(case, similarity(problem, case["problem"]))
              for case in case_base]
    for case, score in scored:
        print(f"  {case['id']}: similarity = {score:.2%}")
    return max(scored, key=lambda item: item[1])


def reuse(case):
    """Start with the retrieved case's existing solution."""
    return case["solution"]


def revise(solution, replacement):
    """Keep the solution when the user submits an empty response."""
    return replacement.strip() or solution


def retain(case_base, problem, solution):
    """Store an independent copy for reuse during this program session."""
    case = {"id": f"C{len(case_base) + 1}",
            "problem": deepcopy(problem), "solution": solution}
    case_base.append(case)
    return case


def main(demo=False):
    # Working memory contains the current classroom observations.
    facts, case_base = deepcopy(FACTS), deepcopy(CASE_BASE)
    print("TA4 | CLASSROOM COMFORT ADVISER")
    print("INPUT: current classroom facts")
    for category, values in facts.items():
        print(f"  {category}: {values}")

    print("\nRBR PROCESS: check all three rules")
    actions = infer(facts)
    print("Rule-Based Reasoning Actions:")
    for action in actions:
        print(f"- {action}")
    if not actions:
        print("- No actions inferred.")

    print("\nCBR PROCESS: RETRIEVE")
    case, score = retrieve(facts, case_base)
    print(f"Selected case: {case['id']} ({score:.2%})")
    solution = reuse(case)
    print(f"REUSE: {solution}")
    if demo:
        # Scripted manual revision to make the report reproducible.
        replacement = solution + " Turn on the aircon."
        print(f"REVISE (demo input): {replacement}")
    else:
        replacement = input("REVISE: new solution, or Enter to keep: ")
    solution = revise(solution, replacement)
    print(f"Final CBR solution: {solution}")
    new_case = retain(case_base, facts, solution)
    print(f"RETAIN: added {new_case['id']}; case count = {len(case_base)}")
    print("Retention is in memory for this run; no file is written.")
    print("\nVerification: retrieve the same problem after retention")
    best, score = retrieve(facts, case_base)
    print(f"Selected case: {best['id']} ({score:.2%})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true",
                        help="Use the report's scripted revision.")
    main(parser.parse_args().demo)
