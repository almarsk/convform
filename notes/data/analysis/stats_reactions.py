from scipy.stats import mannwhitneyu
import numpy as np
import scipy.stats as stats
import json
import pandas as pd

with open("notes/data/final_annotated_data.json", "r") as d:
    data = json.load(d)

    def get_reaction_stats(stimulus_type: str):
        result = [0,0,0]
        reactions = [c["user_reaction"] for c in data if
            "user_reaction" in c  and
            "stimulus" in c and c["stimulus"] == stimulus_type]

        for r in reactions:
            if r == "continuation":
                result[0] += 1
            elif r == "meta":
                result[1] += 1
            elif r == "abort":
                result[2] += 1

        return result


    data = {
        'shallow': get_reaction_stats('shallow'),
        'deep': get_reaction_stats('deep'),
        'nonassignable': get_reaction_stats('nonassignable')
    }

    # Create a pandas DataFrame
    df = pd.DataFrame(data, index=['continuation', 'meta', 'abort'])

    print(df)

    # Perform the Chi-Square test
    chi2, p, dof, expected = stats.chi2_contingency(df)

    print(f"Chi2 Statistic: {chi2}")
    print(f"P-value: {p}")
    print(f"Degrees of Freedom: {dof}")
    print(f"Expected Frequencies: \n{expected}")
