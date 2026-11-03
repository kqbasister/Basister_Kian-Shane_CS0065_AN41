from fractions import Fraction


DATA = [2, 4, 10, 12, 3, 20, 30, 11, 25]


def assign_clusters(data, means):
    clusters = [[], []]
    distances = []
    for value in data:
        d1, d2 = (abs(value - mean) for mean in means)
        index = 0 if d1 <= d2 else 1  # A tie goes to C1.
        clusters[index].append(value)
        distances.append((value, d1, d2, index + 1))
    return clusters, distances


def update_means(clusters, previous):
    # Retain the previous centroid if a cluster is empty.
    return [Fraction(sum(cluster), len(cluster)) if cluster else old
            for cluster, old in zip(clusters, previous)]


def main():
    means = [Fraction(4), Fraction(11)]
    print("TECHNICAL 7 - K-MEANS (K=2)")
    print(f"Data: {DATA}")
    print("Iteration 1 uses the worksheet's initial centroids 4 and 11.")
    for iteration in range(1, 4):
        print(f"\nITERATION {iteration}")
        print(f"Starting means: M1={float(means[0]):.6f}, M2={float(means[1]):.6f}")
        clusters, distances = assign_clusters(DATA, means)
        print(f"{'Point':>6} {'D1':>12} {'D2':>12} {'Cluster':>9}")
        for value, d1, d2, cluster in distances:
            print(f"{value:>6} {float(d1):>12.6f} {float(d2):>12.6f} {'C'+str(cluster):>9}")
        new_means = update_means(clusters, means)
        for index, (cluster, mean) in enumerate(zip(clusters, new_means), 1):
            print(f"C{index} = {cluster}")
            print(f"New M{index} = {sum(cluster)}/{len(cluster)} = {float(mean):.6f}")
        if new_means == means:
            print("Centroids are unchanged: converged.")
        means = new_means


if __name__ == "__main__":
    main()
