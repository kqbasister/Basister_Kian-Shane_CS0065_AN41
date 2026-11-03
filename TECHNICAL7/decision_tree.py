"""Technical 7: learn an unpruned ID3 tree from weighted planet observations.

Run: python decision_tree.py
Uses only Python's standard library; no CODIO or extra packages are needed.
"""

from collections import Counter
from html import escape
from math import log2
from pathlib import Path


# Size, Orbit, Habitable, Count (the eight rows represent 800 planets).
DATA = [
    {"Size": "Big", "Orbit": "Near", "Habitable": "Yes", "Count": 20},
    {"Size": "Big", "Orbit": "Far", "Habitable": "Yes", "Count": 170},
    {"Size": "Small", "Orbit": "Near", "Habitable": "Yes", "Count": 139},
    {"Size": "Small", "Orbit": "Far", "Habitable": "Yes", "Count": 45},
    {"Size": "Big", "Orbit": "Near", "Habitable": "No", "Count": 130},
    {"Size": "Big", "Orbit": "Far", "Habitable": "No", "Count": 30},
    {"Size": "Small", "Orbit": "Near", "Habitable": "No", "Count": 11},
    {"Size": "Small", "Orbit": "Far", "Habitable": "No", "Count": 255},
]


def class_counts(rows):
    counts = Counter()
    for row in rows:
        counts[row["Habitable"]] += row["Count"]
    return counts


def entropy(rows):
    counts = class_counts(rows)
    total = sum(counts.values())
    return -sum((n / total) * log2(n / total) for n in counts.values() if n)


def partitions(rows, attribute):
    groups = {}
    for row in rows:
        groups.setdefault(row[attribute], []).append(row)
    return groups


def information_gain(rows, attribute):
    total = sum(row["Count"] for row in rows)
    remainder = sum(
        sum(row["Count"] for row in group) / total * entropy(group)
        for group in partitions(rows, attribute).values()
    )
    return entropy(rows) - remainder


def id3(rows, attributes):
    counts = class_counts(rows)
    # Majority vote labels mixed leaves when no attributes remain.
    prediction = max(("Yes", "No"), key=lambda label: counts[label])
    node = {"counts": counts, "prediction": prediction}
    if len([n for n in counts.values() if n]) == 1 or not attributes:
        return node
    best = max(attributes, key=lambda attribute: information_gain(rows, attribute))
    node["attribute"] = best
    node["children"] = {
        value: id3(group, [attribute for attribute in attributes if attribute != best])
        for value, group in partitions(rows, best).items()
    }
    return node


def predict(tree, sample):
    node = tree
    while "attribute" in node:
        value = sample[node["attribute"]]
        node = node["children"][value]
    return node["prediction"]


def print_tree(node, indent=""):
    if "attribute" not in node:
        print(f"{indent}Habitable: {node['prediction']} "
              f"(Yes={node['counts']['Yes']}, No={node['counts']['No']})")
        return
    print(f"{indent}Split: {node['attribute']}")
    for value, child in node["children"].items():
        print(f"{indent}  [{value}]")
        print_tree(child, indent + "    ")


def save_tree_svg(tree, path):
    """Draw the learned tree as an editable, dependency-free SVG."""
    leaves = []
    nodes = []
    edges = []

    def layout(node, depth):
        children = []
        for label, child in node.get("children", {}).items():
            children.append((label, layout(child, depth + 1)))
        if children:
            x = sum(child[0] for _, child in children) / len(children)
        else:
            x = 160 + 300 * len(leaves)
            leaves.append(node)
        y = 145 + depth * 170
        for label, child in children:
            edges.append((x, y, child[0], child[1], label))
        nodes.append((x, y, node))
        return x, y

    layout(tree, 0)
    width = max(640, 300 * len(leaves) + 20)
    height = max(y for _, y, _ in nodes) + 130
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="white"/>',
           '<g font-family="Arial, sans-serif" text-anchor="middle" fill="#172b4d">',
           f'<text x="{width/2}" y="45" font-size="28" font-weight="bold">'
           'Technical 7: Planet Habitability - ID3</text>',
           f'<text x="{width/2}" y="78" font-size="17">'
           '800 observations | Maximum information gain | No pruning</text>']
    for x, y, cx, cy, label in edges:
        svg.append(f'<path d="M {x} {y+42} L {cx} {cy-42}" stroke="#65758b" '
                   'stroke-width="2" fill="none"/>')
        mx, my = (x + cx) / 2, (y + cy) / 2
        svg.append(f'<rect x="{mx-34}" y="{my-15}" width="68" height="28" fill="white"/>')
        svg.append(f'<text x="{mx}" y="{my+5}" font-size="18">{escape(label)}</text>')
    for x, y, node in nodes:
        internal = "attribute" in node
        color = "#eaf0fc" if internal else ("#e7f5eb" if node["prediction"] == "Yes" else "#fff0e7")
        title = f'Split: {node["attribute"]}' if internal else f'Habitable: {node["prediction"]}'
        svg.append(f'<rect x="{x-133}" y="{y-42}" width="266" height="84" rx="12" '
                   f'fill="{color}" stroke="#65758b"/>')
        svg.append(f'<text x="{x}" y="{y-6}" font-size="22" font-weight="bold">{escape(title)}</text>')
        svg.append(f'<text x="{x}" y="{y+23}" font-size="18">'
                   f'Yes: {node["counts"]["Yes"]} | No: {node["counts"]["No"]}</text>')
    svg.append(f'<text x="{width/2}" y="{height-30}" font-size="16">'
               'Yes = habitable; No = not habitable. Mixed leaves use the majority class.</text>')
    svg.append('</g></svg>')
    path.write_text("\n".join(svg), encoding="utf-8")


def main():
    print("TECHNICAL 7 - ID3 DECISION TREE")
    print(f"Total planets: {sum(row['Count'] for row in DATA)}")
    print(f"Initial entropy: {entropy(DATA):.6f} bits")
    for attribute in ("Size", "Orbit"):
        print(f"Information gain ({attribute}): {information_gain(DATA, attribute):.6f}")
    tree = id3(DATA, ["Size", "Orbit"])
    for size, group in partitions(DATA, "Size").items():
        print(f"Information gain (Orbit | Size={size}): {information_gain(group, 'Orbit'):.6f}")
    print()
    print_tree(tree)
    for size, orbit in (("Big", "Far"), ("Small", "Near")):
        result = predict(tree, {"Size": size, "Orbit": orbit})
        print(f"\nSize={size}, Orbit={orbit} -> Habitable: {result}")
    path = Path(__file__).with_name("decision_tree.svg")
    save_tree_svg(tree, path)
    print(f"\nDiagram saved to: {path.name}")


if __name__ == "__main__":
    main()
