import json
import pprint

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
    print("Design rating")
    print("______________")

    def print_stimulus_ratio():
        ratio = []
        for stimulus_type in ["shallow", "deep", "nonassignable"]:
            ratio.append(len([c for c in data if
                "stimulus" in c and c["stimulus"] == stimulus_type
                ]))
        print(f"Ratio stimulus s:d:n {ratio[0]}:{ratio[1]}:{ratio[2]}")
    print_stimulus_ratio()

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
        print(f"Ratio stimulus null rating s:d:n {ratio[0]}:{ratio[1]}:{ratio[2]}")
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
        print(f"Rating incl null {get_design_mask(stimulus_type)} {rating_avg}")
    run_for_all_designs(print_rating_avg_with_null_direct)

    def get_rating_difference_with_without_null_direct(stimulus_type: str):
        return get_rating_avg(stimulus_type) - get_rating_avg_with_null_direct(stimulus_type)
    def print_rating_difference_with_without_null_direct(stimulus_type: str):
        print(f"Rating diff nonull vs null {get_design_mask(stimulus_type)} {get_rating_difference_with_without_null_direct(stimulus_type)}")
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
        print(f"Rating diff nonull vs null {get_design_mask(stimulus_type)} {get_rating_difference_with_without_null_anytime(stimulus_type)}")

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
    print(f"stimulus zero anaphora s:d:n {ratio[0]:02}:{ratio[1]:02}:{ratio[2]:02}")

    def get_zero_anaphora_reaction_ratio():
        ratio = []
        for reaction in ["continuation", "meta", "abort"]:
            ratio.append(len([c for c in data if
                "zero_anaphora" in c and c["zero_anaphora"] and
                "user_reaction" in c and c["user_reaction"] == reaction]))
        return ratio

    ratio = get_zero_anaphora_reaction_ratio()
    print(f"rating zero anaphora c:m:a {ratio[0]:02}:{ratio[1]:02}:{ratio[2]:02}\n")

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
        print(f"Reaction ratio {get_design_mask(stimulus_type)} c:m:a {ratio[0]:02}:{ratio[1]:02}:{ratio[2]:02}")

    run_for_all_designs(print_reaction_ratio)

    def print_percentage_ratio_reaction(stimulus_type):
        ratio = get_reaction_ratio(stimulus_type)
        total = sum(ratio)
        percentages = [(x / total) * 100 for x in ratio]
        print(f"Percentage ratio {get_design_mask(stimulus_type)} {percentages[0]:.2f}% : {percentages[1]:.2f}% : {percentages[2]:.2f}%")

    run_for_all_designs(print_percentage_ratio_reaction)
