from joblib import Parallel, delayed
import json
import re
import yaml


def match_template(s, tmpls):
    matches = [(tmpl["id"], re.search(tmpl["regex"], s)) for tmpl in tmpls]
    matches = [(t, m.groupdict()) if m else (t, {}) for t, m in matches]
    return max(matches, key=lambda x: len(x[1]))


if __name__ == "__main__":
    with open("qa_templates.yaml", "r") as fin:
        tmpls = yaml.safe_load(fin)
    with open("data/qa_ns_1.json", "r") as fin:
        qa = json.load(fin)

    res = Parallel(n_jobs=-1, verbose=2)(
        delayed(match_template)(k["question_string"], tmpls) for k in qa
    )
    res = [
        {"question_id": q["question_id"], "regex": k[0], "matches": k[1]}
        for q, k in zip(qa, res)
    ]
    with open("data/matches_1.json", "w") as fout:
        json.dump(res, fout, indent=2)
