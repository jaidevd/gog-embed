import os
from PIL import Image
import re
import random
from pydoc import locate
from tornado.template import Template
import yaml
import pandas as pd

op = os.path
with open("qa_templates.yaml", "r") as fin:
    tmpl_cfg = pd.DataFrame.from_records(yaml.safe_load(fin), index="id")


def match_template(s, tmpls):
    matches = [re.search(pat, s) for pat in tmpls]
    matches = [m.groupdict() if m else {} for m in matches]
    return max(matches, key=len)


def generate_caption(header, caption, answer, **kwargs):
    tmpl = header
    if isinstance(caption, list):
        tmpl += random.choice(caption)
    elif isinstance(caption, str):
        func = locate(caption)
        if callable(func):
            tmpl += func(answer)
        else:
            tmpl += caption
    else:
        raise ValueError(f"Invalid caption template {caption}.")

    return Template(tmpl).generate(answer=answer, **kwargs).decode()


def process_qa(question_id, regex, answer, matches):
    if answer is None:
        return {"question_id": question_id, "template_id": regex, "caption": ""}
    tmpl = tmpl_cfg.loc[regex]
    header = tmpl["template_header"]
    caption = tmpl["caption_templates"]
    try:
        if len(matches):
            out = generate_caption(header, caption, answer, **matches)
        else:
            out = ""
    except Exception as exc:
        print(f"Failed for tid: {regex} qid: {question_id}")
        print(caption)
        print(matches)
        raise exc
    return {"question_id": question_id, "template_id": regex, "caption": out}


class PlotQA(object):
    def __init__(self, root):
        self.root = root

    def load_qa(self, by="chart-id"):
        pass

    def show(self, chart_id):
        path = op.join(self.root, "png", f"{chart_id}.png")
        with Image.open(path) as im:
            im.show()


if __name__ == "__main__":
    from joblib import Parallel, delayed
    import json

    with open("data/matches_merged_2.json", "r") as fin:
        df = json.load(fin)

    res = Parallel(n_jobs=-1, verbose=2)(delayed(process_qa)(**row) for row in df)
    with open("data/captions_2.json", "w") as fout:
        json.dump(res, fout, indent=2)
