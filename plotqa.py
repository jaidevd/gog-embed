import os
from PIL import Image
import re
import random
from pydoc import locate
from tornado.template import Template
import yaml
import pandas as pd
from grammar import fix

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


def match_and_generate(qs, answer, pattern, header, tmpl_opts):
    matches = re.search(pattern, qs)
    if matches:
        matches = matches.groupdict()
    else:
        return ''
    tmpl = header
    if isinstance(tmpl_opts, list):
        tmpl += random.choice(tmpl_opts)
    elif isinstance(tmpl_opts, str):
        func = locate(tmpl_opts)
        if callable(func):
            tmpl += func(answer)
        else:
            tmpl += tmpl_opts
    else:
        raise ValueError(f"Invalid caption template {tmpl_opts}.")
    return Template(tmpl).generate(answer=answer, **matches).decode()


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

    tmpl = tmpl_cfg.loc[1]
    header = tmpl["template_header"]
    tmpl_opts = tmpl["caption_templates"]
    pattern = tmpl["regex"]

    def _proc(question_string, answer, question_id, **kwargs):
        caption = match_and_generate(
            question_string, answer, pattern, header, tmpl_opts
        )
        return {
            "question_id": question_id,
            "caption": fix(caption),
        }

    for i, df in enumerate(
        pd.read_json("data/qa_captions.json", lines=True, chunksize=1_000_000)
    ):
        eights = df[df["template_id"] == 1]
        if len(eights) > 0:
            captions = Parallel(n_jobs=-1, verbose=1)(
                delayed(_proc)(**row) for _, row in eights.iterrows()
            )
            captions = (
                pd.DataFrame(captions)
                .set_index("question_id", verify_integrity=True)
                .squeeze("columns")
            )
            df.set_index("question_id", verify_integrity=True, inplace=True)
            df.loc[captions.index, "caption"] = captions
            df.reset_index().to_json(
                f"data/qa_captions_1fix_{i}.json", lines=True, orient="records"
            )
        else:
            df.to_json(f"data/qa_captions_1fix_{i}.json", lines=True, orient="records")

    # import json

    # with open("data/matches_merged_2.json", "r") as fin:
    #     df = json.load(fin)

    # res = Parallel(n_jobs=-1, verbose=2)(delayed(process_qa)(**row) for row in df)
    # with open("data/captions_2.json", "w") as fout:
    #     json.dump(res, fout, indent=2)
