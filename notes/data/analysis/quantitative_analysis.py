import json
import pprint
import matplotlib.pyplot as plt
from itertools import combinations
from sklearn.metrics import cohen_kappa_score
import numpy as np
import pandas as pd
import os
import scipy.stats as stats

def run_for_all_designs(fun):
    fun("shallow")
    fun("deep")
    fun("nonassignable")
    print()

design_mask = {
    "shallow": "shlw",
    "deep": "deep",
    "nonassignable": "nass"
}

def get_design_mask(s):
    return design_mask[s]


with open("notes/data/final_annotated_data.json", "r") as d:
    data = json.load(d)

    print(f"Number of convos: {len(data)}")

    print("______________")
    print("Rating range")
    print("______________")

    ratings = {}
    _rated = [c["rating"] for c in data
        if "rating" in c and c["rating"] and
        "stimulus" in c and c["stimulus"] in ["shallow", "deep", "nonassignable"]
    ]
    ratings = {i: _rated.count(i) for i in range(1, 6)}
    print("Ratings between 1 and 5:")
    for rating, count in sorted(ratings.items()):
        print(f"Rating {rating}: {count} times")

    no_rating = len([c["rating"] for c in data
        if "rating" in c and not c["rating"] and
        "stimulus" in c and c["stimulus"] in ["shallow", "deep", "nonassignable"]
    ])
    print(f"No rating: {no_rating} times")

    def plot_rating_distribution():
        ratings_list = [rating for rating, count in ratings.items() for _ in range(count)]
        plt.hist(ratings_list, bins=range(1, 7), align='left', color='skyblue', edgecolor='black')
        plt.xlabel("Rating")
        plt.ylabel("Frequency")
        plt.title("Rating Distribution")
        plt.xticks(range(1, 6))  # Ensure all ratings are labeled
        plt.show()

    print("______________")
    print("Design rating")
    print("______________")

    def print_stimulus_ratio():
        ratio = []
        for stimulus_type in ["shallow", "deep", "nonassignable", "other"]:
            ratio.append(len([c for c in data if
                "stimulus" in c and c["stimulus"] == stimulus_type
                ]))
        print(f"Ratio stimulus shallow:deep:nonassignable:other {ratio[0]}:{ratio[1]}:{ratio[2]}:{ratio[3]}")
    print_stimulus_ratio()

    def print_stimulus_ratio_rating_check():
        ratio = []
        for stimulus_type in ["shallow", "deep", "nonassignable", "other"]:
            ratio.append(len([c for c in data if
                "rating" in c and c["rating"] and
                "stimulus" in c and c["stimulus"] == stimulus_type
                ]))
        print(f"Ratio stimulus rating check shallow:deep:nonassignable:other {ratio[0]}:{ratio[1]}:{ratio[2]}:{ratio[3]}")
    print_stimulus_ratio_rating_check()

    def get_rating_avg(stimulus_type: str):
        _rated = [c["rating"] for c in data if
            "rating" in c and c["rating"] and
            "stimulus" in c and stimulus_type == c["stimulus"]
        ]
        _sum_score = sum([c for c in _rated])
        rating_avg = _sum_score/len(_rated)
        return rating_avg

    def print_rating_avg(stimulus_type: str):
        rating_avg = get_rating_avg(stimulus_type)
        print(f"Rating {get_design_mask(stimulus_type)} {rating_avg}")

    run_for_all_designs(print_rating_avg)

    def print_stimulus_ratio_null_rating():
        ratio = []
        for stimulus_type in ["shallow", "deep", "nonassignable"]:
            ratio.append(len([c for c in data if
                not c["rating"] and
                "stimulus" in c and c["stimulus"] == stimulus_type
                ]))
        print(f"Ratio stimulus null rating shallow:deep:nonassignable {ratio[0]}:{ratio[1]}:{ratio[2]}")
    print_stimulus_ratio_null_rating()

    def get_rating_avg_with_null_direct(stimulus_type: str):
        _rated = [(c["rating"] or 5) for c in data if
            "rating" in c and
            "stimulus" in c and stimulus_type == c["stimulus"] and
            "user_reaction" in c and (c["user_reaction"] == "abort" or c["rating"])]
        _sum_score = sum([c for c in _rated])

        rating_avg = _sum_score/len(_rated)
        return rating_avg
    def print_rating_avg_with_null_direct(stimulus_type: str):
        rating_avg = get_rating_avg_with_null_direct(stimulus_type)
        print(f"Rating incl null direct {get_design_mask(stimulus_type)} {rating_avg}")
    run_for_all_designs(print_rating_avg_with_null_direct)

    def get_rating_difference_with_without_null_direct(stimulus_type: str):
        return get_rating_avg(stimulus_type) - get_rating_avg_with_null_direct(stimulus_type)
    def print_rating_difference_with_without_null_direct(stimulus_type: str):
        print(f"Rating diff nonull vs null direct {get_design_mask(stimulus_type)} {get_rating_difference_with_without_null_direct(stimulus_type)}")
    run_for_all_designs(print_rating_difference_with_without_null_direct)

    def get_rating_avg_with_null_anytime(stimulus_type: str):
        _rated = [(c["rating"] or 5) for c in data if
            "rating" in c and
            "stimulus" in c and stimulus_type == c["stimulus"]
           ]
        _sum_score = sum([c for c in _rated])

        rating_avg = _sum_score/len(_rated)
        return rating_avg
    def print_rating_avg_with_null_anytime(stimulus_type: str):
        rating_avg = get_rating_avg_with_null_anytime(stimulus_type)
        print(f"Rating incl null anytime {get_design_mask(stimulus_type)} {rating_avg}")
    run_for_all_designs(print_rating_avg_with_null_anytime)

    def get_rating_difference_with_without_null_anytime(stimulus_type: str):
        return get_rating_avg(stimulus_type) - get_rating_avg_with_null_anytime(stimulus_type)
    def print_rating_difference_with_without_null_anytime(stimulus_type: str):
        print(f"Rating diff nonull vs null anytime {get_design_mask(stimulus_type)} {get_rating_difference_with_without_null_anytime(stimulus_type)}")

    run_for_all_designs(print_rating_difference_with_without_null_anytime)

    print("______________")
    print("Zero anaphora")
    print("______________")

    zero_anaphora_number = len([convo for convo in data if 'zero_anaphora' in convo and convo['zero_anaphora']])
    print(f"Number of zero anaphora conversations: {zero_anaphora_number}")

    def get_zero_anaphora_stimulus_type():
        ratio = []
        for reaction in ["shallow", "deep", "nonassignable"]:
            ratio.append(len([c for c in data if
                "zero_anaphora" in c and c["zero_anaphora"] and
                "stimulus" in c and c["stimulus"] == reaction]))
        return ratio

    ratio = get_zero_anaphora_stimulus_type()
    print(f"stimulus zero anaphora shallow:deep:nonassignable {ratio[0]:02}:{ratio[1]:02}:{ratio[2]:02}")

    def get_zero_anaphora_reaction_ratio():
        ratio = []
        for reaction in ["continuation", "meta", "abort"]:
            ratio.append(len([c for c in data if
                "zero_anaphora" in c and c["zero_anaphora"] and
                "user_reaction" in c and c["user_reaction"] == reaction]))
        return ratio

    ratio = get_zero_anaphora_reaction_ratio()
    print(f"Rating zero anaphora continuation:meta:abort {ratio[0]:02}:{ratio[1]:02}:{ratio[2]:02}\n")

    def get_rating_non_zero_anaphora():
        _rated = [c["rating"] for c in data if
            "rating" in c and c["rating"] and
            "stimulus" in c and c["stimulus"] in ["shallow", "deep"] and
            "zero_anaphora" in c and not c["zero_anaphora"]]
        _sum_score = sum([c for c in _rated])
        rating_avg = _sum_score/len(_rated)
        return rating_avg

    def get_rating_zero_anaphora():
        _rated = [c["rating"] for c in data if
            "rating" in c and c["rating"] and
            "stimulus" in c and c["stimulus"] in ["shallow", "deep"] and
            "zero_anaphora" in c and c["zero_anaphora"]]
        _sum_score = sum([c for c in _rated])
        rating_avg = _sum_score/len(_rated)
        return rating_avg

    def print_rating_zero_anaphora():
        print(f"Rating zero anaphora {get_rating_zero_anaphora()}")
        print(f"Rating non zero anaphora {get_rating_non_zero_anaphora()}")

    print_rating_zero_anaphora()


    print("______________")

    print("Reaction ratio")
    print("______________")

    def get_reaction_ratio(stimulus_type: str):
        ratio = []

        for reaction in ["continuation", "meta", "abort"]:
            ratio.append(len([c for c in data if
                "stimulus" in c and c["stimulus"] == stimulus_type and
                "user_reaction" in c and c["user_reaction"] == reaction]))

        return ratio

    def print_reaction_ratio(stimulus_type: str):
        ratio = get_reaction_ratio(stimulus_type)
        print(f"Reaction ratio {get_design_mask(stimulus_type)} continuation:meta:abort {ratio[0]:02}:{ratio[1]:02}:{ratio[2]:02}")

    run_for_all_designs(print_reaction_ratio)

    def print_percentage_ratio_reaction(stimulus_type):
        ratio = get_reaction_ratio(stimulus_type)
        total = sum(ratio)
        percentages = [(x / total) * 100 for x in ratio]
        print(f"Reaction percentage ratio {get_design_mask(stimulus_type)} {percentages[0]:.2f}% : {percentages[1]:.2f}% : {percentages[2]:.2f}%")

    run_for_all_designs(print_percentage_ratio_reaction)

    print("______________")

    print("Stimulus x Reaction specific ratings")
    print("______________")

    def stimulus_reaction_specific_rating():
        print("     | cntn | meta | abrt |")
        for stimulus_type in ["shallow", "deep", "nonassignable"]:
            ratings = list()

            for reaction in ["continuation", "meta", "abort"]:
                convos = [c for c in data if
                    "rating" in c and c["rating"] and
                    "stimulus" in c and c["stimulus"] == stimulus_type and
                    "user_reaction" in c and c["user_reaction"] == reaction]
                score_sum = sum([(c["rating"] or 0) for c in convos if "rating" in c])
                len_convos = len(convos)
                ratings.append([score_sum/len_convos, len_convos])


            avg_stimulus_and_reaction = sum([c[0]*c[1] for c in ratings])/sum([c[1] for c in ratings])
            avg_only_stimulus = get_rating_avg(stimulus_type)

            print(f"{get_design_mask(stimulus_type)} | {ratings[0][0]:.2f} | {ratings[1][0]:.2f} | {ratings[2][0]:.2f} | stimulus x stimulus reaction match {avg_stimulus_and_reaction == avg_only_stimulus}")

    stimulus_reaction_specific_rating()


    print("______________")
    print("Comments")
    print("______________")

    print("Types of comments:")
    comments = [c for c in data if "comment_annot" in c and "stimulus addressed in comment" in c["comment_annot"]]
    print(f"Stimulus mentioned in comments {len(comments)} times")

    for stimulus, mentions in {
        "shallow": len([c for c in comments if "stimulus" in c and c["stimulus"] == "shallow"]),
        "deep": len([c for c in comments if "stimulus" in c and c["stimulus"] == "deep"]),
        "nonassignable": len([c for c in comments if "stimulus" in c and c["stimulus"] == "nonassignable"]),
    }.items():
        print(f"{get_design_mask(stimulus)} mentioned {mentions:02} times in comments")



    print("______________")
    print("Conversation style")
    print("______________")

    def get_conversation_style_convos(conversation_style: str):
        return [c for c in data if conversation_style in c["type"]]

    relaxed = get_conversation_style_convos('relaxed')
    inquisitive = get_conversation_style_convos('inquisitive')

    print(f"Relaxed style convos {len(relaxed)}")
    print(f"Inquisitive style convos {len(inquisitive)}")

    def get_avg_rating(convos):
        return sum([c["rating"] for c in convos if "rating" in c and c["rating"]])/len(convos)

    print(f"Relaxed style rating {get_avg_rating(relaxed):.2f}")
    print(f"Inquisitive style rating {get_avg_rating(inquisitive):.2f}")

    print("Relaxed style addressed in comments: 1x positive 1x negative")
    print("Inquistive style addressed in comments: 1x negative")
