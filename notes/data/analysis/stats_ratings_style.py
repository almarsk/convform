from scipy.stats import mannwhitneyu
import numpy as np
import scipy.stats as stats
import json

with open("notes/data/final_annotated_data.json", "r") as d:
    data = json.load(d)

    def get_group_ratings_with_null(stimulus_type: str):
        return [(c["rating"] or 5) for c in data if
            "rating" in c  and
            "stimulus" in c and c["stimulus"] == stimulus_type]

    def get_group_ratings_no_null(stimulus_type: str):
        return [(c["rating"] or 5) for c in data if
            "rating" in c and c["rating"] and
            "stimulus" in c and c["stimulus"] == stimulus_type]

    def do_stats(ratings_getter):
        group1 = ratings_getter("shallow")  # Group 1's ratings
        group2 = ratings_getter("deep")  # Group 2's ratings
        group3 = ratings_getter("nonassignable")  # Group 3's ratings

        # 2. Kruskal-Wallis Test
        kruskal_stat, kruskal_p = stats.kruskal(group1, group2, group3)

        # 3. Effect Size (Eta Squared)
        # Kruskal-Wallis statistic already available
        # Calculate eta squared (η²)
        total_n = len(group1) + len(group2) + len(group3)
        eta_squared = kruskal_stat / (total_n - 3)  # This is a rough approximation for eta squared

        print(f"\nKruskal-Wallis Test p-value: {kruskal_p}")
        print(f"Effect Size (Eta Squared): {eta_squared}")

        # Combine the groups into a single array and create a group labels array
        data = np.concatenate([group1, group2, group3])
        groups = ['shallow'] * len(group1) + ['deep'] * len(group2) + ['nonassignable'] * len(group3)

        # Perform Dunn's Test (post-hoc pairwise comparison)
        # statsmodels does not directly support Dunn's, but you can use the Mann-Whitney U test pairwise

        def dunn_test(groups, data):
            group_labels = np.unique(groups)
            results = []
            for i in range(len(group_labels)):
                for j in range(i + 1, len(group_labels)):
                    # Perform Mann-Whitney U test between each pair of groups
                    group_i = data[np.array(groups) == group_labels[i]]
                    group_j = data[np.array(groups) == group_labels[j]]
                    stat, p_value = mannwhitneyu(group_i, group_j)
                    results.append((group_labels[i], group_labels[j], p_value))
            return results

        # Run the Dunn's Test
        dunn_results = dunn_test(groups, data)

        # Print Dunn's Test results
        for result in dunn_results:
            print(f"Comparison: {result[0]} vs {result[1]}, p-value: {result[2]}")

    print("For ratings without null:")
    do_stats(get_group_ratings_no_null)
    print("\nFor ratings with null interpreted as 5:")
    do_stats(get_group_ratings_with_null)


    print("____________\nConversation style\n___________")

    def get_style_ratings(stimulus_type: str):
        return [(c["rating"] or 5) for c in data if
            "rating" in c and c["rating"] and
            "type" in c and stimulus_type in c["type"]]

    def do_stats_style(ratings_getter):
        group1 = ratings_getter("inquisitive")  # Group 1's ratings
        group2 = ratings_getter("relaxed")  # Group 2's ratings

        # 2. Kruskal-Wallis Test
        kruskal_stat, kruskal_p = stats.kruskal(group1, group2)

        # 3. Effect Size (Eta Squared)
        # Kruskal-Wallis statistic already available
        # Calculate eta squared (η²)
        total_n = len(group1) + len(group2)
        eta_squared = kruskal_stat / (total_n - 3)  # This is a rough approximation for eta squared

        print(f"\nKruskal-Wallis Test p-value: {kruskal_p}")
        print(f"Effect Size (Eta Squared): {eta_squared}")

    do_stats_style(get_style_ratings)
