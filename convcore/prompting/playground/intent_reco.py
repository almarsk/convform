from ..utilz import get_letter_seq

def intent_reco(prompts, user_speech, log):
    options = "\n".join([f"{get_letter_seq(index+1)}) {prompt}" for index, prompt in enumerate(prompts)])
    task=f"""
    Tady jsou možnosti:

    {options}
    {len(prompts)}) žádná z nabídnutých možností

    Které z uvedených variant nejlépe odpovídá poslední replika v následující konverzaci?
    """

    # return list of dicts - prompt + start index
    # [{ "prompt": str, "match_index": int}]
    return []
