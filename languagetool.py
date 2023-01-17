import json
from requests import get
import gc
import re
from joblib import Parallel, delayed
from tqdm import tqdm


URL = "http://localhost:8081/v2/check"


def process(question_id, caption, template_id=None):
    resp = get(URL, params={"language": "en-US", "text": caption})
    if resp.ok:
        return {"question_id": question_id, "matches": resp.json()["matches"]}
    raise ValueError(f"LT Request failed with status {resp.status_code}")


# Fixes


def fix_spaces(s):
    """
    0. Trim leading and trailing whitespaces.
    1. Don't put a space before the full stop.
    2. Don't have too many consecuitive spaces.
    3. Remove spaces before commas.
    4. Remove unnecessary quoute marks.
    """
    s = s.strip()
    s = re.sub(r"\s+\.", ".", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+,", ",", s)
    s = re.sub(r"^[\'\"]+\s?", "", s)
    return s


def fix_tokens(s):
    """Change typos in arbit tokens."""
    typos = [(r"\bus\$", "USD"), (r"korea", "Korea")]
    for pat, repl in typos:
        s = re.sub(pat, repl, s)
    return s


def fix(s):
    s = fix_spaces(s)
    s = fix_tokens(s)
    return s


def check():
    with open("data/captions_1.json", "r") as fin:
        captions = [k for k in json.load(fin) if k["caption"]]
    unit = 1_000_000
    n_slices = len(captions) // unit
    remainder = len(captions) % unit
    for i in tqdm(range(5, n_slices)):
        gc.collect()
        part = captions[(i * unit): (i + 1) * unit]
        res = Parallel(n_jobs=-1, verbose=2)(delayed(process)(**k) for k in part)
        res = [k for k in res if k["matches"]]
        with open(f"data/lt_results_{i}.json", "w") as fout:
            json.dump(res, fout, indent=2)

    remainder = captions[-remainder:]
    res = Parallel(n_jobs=-1, verbose=2)(delayed(process)(**k) for k in remainder)
    res = [k for k in res if k["matches"]]
    with open("data/lt_results_final.json", "w") as fout:
        json.dump(res, fout, indent=2)


if __name__ == "__main__":
    with open("data/captions_2.json", "r") as fin:
        captions = json.load(fin)

    def _proc(x):
        x.update({'caption': fix(x['caption'])})
        return x

    res = Parallel(n_jobs=-1, verbose=2)(delayed(_proc)(c) for c in captions)

    with open("data/captions_2.json", "w") as fin:
        json.dump(res, fin, indent=2)
