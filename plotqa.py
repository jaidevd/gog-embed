import os
from PIL import Image
import re
import random
from pydoc import locate
from tornado.template import Template
import yaml
import pandas as pd
import warnings

# from grammar import fix
# from pymongo import MongoClient, UpdateMany
# from tqdm import tqdm
# import bson

op = os.path
with open("qa_templates.yaml", "r") as fin:
    tmpl_cfg = pd.DataFrame.from_records(yaml.safe_load(fin), index="id")


def search_templates(tmpls, _id, question_string, **kwargs):
    matches = [(tmpl["id"], re.search(tmpl["regex"], question_string)) for tmpl in tmpls]
    matches = [(t, m.groupdict()) if m else (t, {}) for t, m in matches]
    match = max(matches, key=lambda x: len(x[1]))
    if len(match[1]) == 0:
        warnings.warn(f"Question ID {_id} didn't match any template.")
    return {"_id": _id, "template_id": match[0], "matches": match[1]}


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
        return ""
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
    from pymongo import MongoClient, UpdateOne
    from joblib import Parallel, delayed
    import bson

    tmpls = tmpl_cfg[["regex"]].reset_index().to_dict(orient="records")
    with MongoClient() as client:
        db = client.plotqa
        for batch in db.val_captions.find_raw_batches({'varmatchsize': 0}, batch_size=1_000_000):
            docs = bson.decode_all(batch)
            res = Parallel(n_jobs=-1, verbose=2)(
                delayed(search_templates)(tmpls, **doc) for doc in docs
            )
            updates = [
                UpdateOne(
                    {"_id": r["_id"]},
                    {
                        "$set": {
                            "variables": r["matches"],
                            "template_id": r["template_id"],
                            "varmatchsize": len(r["matches"]),
                        }
                    },
                )
                for r in res
            ]
            wres = db.val_captions.bulk_write(updates)
            print(wres.bulk_api_result)
