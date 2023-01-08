from joblib import Parallel, delayed
import json
import re
import yaml


def match_template(s, tmpls):
    matches = [re.search(pat, s) for pat in tmpls]
    matches = [m.groupdict() if m else {} for m in matches]
    return max(zip(tmpls, matches), key=lambda x: len(x[1]))


if __name__ == "__main__":
    with open("data/qa_ns_2.json", "r") as fin:
        qa = json.load(fin)
    with open("qa_templates.yaml", "r") as fin:
        tmpls = yaml.safe_load(fin)
    tmpls = tmpls["retrieval"] + tmpls["reasoning"]
    res = Parallel(n_jobs=-1, verbose=2)(
        delayed(match_template)(k["question_string"], tmpls) for k in qa
    )
    res = [
        {'question_id': q['question_id'], 'regex': k[0], 'matches': k[1]} for q, k in zip(qa, res)
    ]
    with open('data/matches_2.json', 'w') as fout:
        json.dump(res, fout, indent=2)
