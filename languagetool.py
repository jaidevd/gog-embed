import json
from requests import get
import gc
import re
from joblib import Parallel, delayed
from tqdm import tqdm
from spacy.tokens import Doc


URL = "http://localhost:8081/v2/check"


def process(question_id, caption, template_id=None, **kwargs):
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


def space_before_bracket(s):
    return re.sub(r'(?P<prefix>\S)\(', r'\g<prefix> (', s)


def missing_determiner(s, repl, offset, length):
    """
    Gambia, The
    """
    prefix = s[:offset]
    suffix = s[(offset + length):]
    return prefix + repl + suffix


def determiner_suffix_nnp(s):
    """Fix proper nouns when determiners appear at the end, like:

    United States of America, The
    Czech Republic, The
    """
    return re.sub(r'(?P<nnp>.*), The', r'The \g<nnp>', s)


def unpaired_symbol(s, sym):
    count = s.count(sym)
    if count > 0 and s.count(sym) % 2 == 0:
        msg = f'Symbol {sym} is not unpaired in the sentence:\n' + s
        raise ValueError(msg)
    raise NotImplementedError


def trim_leading_symbols(s, sym='"'):
    count = s.count(sym)
    if count > 0 and s.count(sym) % 2 == 0:
        msg = f'Symbol {sym} is not unpaired in the sentence:\n' + s
        raise ValueError(msg)
    return re.sub(f'^\\s*{sym}\\s*', '', s)


def fix(s):
    s = fix_spaces(s)
    s = fix_tokens(s)
    return s


def repeated_words(s):
    """
    in in 2008?
    in in 2006 to ...
    in in Ecuador
    in in North America
    Messed Up:
        - Spain the -> Spain in the
        - Benin
        - Bahrain the
        - Liechtenstein
        - origin
    """


def fix_is_subject(s):
    """
    ('The verb form ‘is’ does not seem to match the subject ‘exports’.', 89),
    ('The verb form ‘is’ does not seem to match the subject ‘savings’.', 19),
    ('The verb form ‘is’ does not seem to match the subject ‘withdrawals’.', 17),
    ('The verb form ‘is’ does not seem to match the subject ‘remittances’.', 9),
    ('The verb form ‘is’ does not seem to match the subject ‘stocks’.', 5),
    ('The verb form ‘differ’ does not seem to match the subject ‘rent’.', 4),
    ('The verb form ‘does’ does not seem to match the subject ‘withdrawals’.', 2),
    ('The verb form ‘does’ does not seem to match the subject ‘savings’.', 2),
    ('The verb form ‘does’ does not seem to match the subject ‘payments’.', 2),
    ('The verb form ‘differ’ does not seem to match the subject ‘education’.', 2),
    ('The verb form ‘differ’ does not seem to match the subject ‘service’.', 2),
    ('The verb form ‘differ’ does not seem to match the subject ‘rate’.', 2),
    ('The verb form ‘differ’ does not seem to match the subject ‘ratio’.', 2),
    ('The verb form ‘is’ does not seem to match the subject ‘payments’.', 1),
    ('The verb form ‘does’ does not seem to match the subject ‘imports’.', 1),
    ('The verb form ‘does’ does not seem to match the subject ‘remittances’.', 1),
    ('The verb form ‘increases’ does not seem to match the subject ‘savings’.',
     1),
    ('The verb form ‘does’ does not seem to match the subject ‘flows’.', 1),
    ('The verb form ‘does’ does not seem to match the subject ‘stocks’.', 1),
    ('The verb form ‘differ’ does not seem to match the subject ‘population’.',
     1),
    ('The verb form ‘differ’ does not seem to match the subject ‘density’.', 1),
    ('The verb form ‘differ’ does not seem to match the subject ‘students’.', 1),
    ('The verb form ‘differ’ does not seem to match the subject ‘production’.',
     1),
    ('The verb form ‘differ’ does not seem to match the subject ‘index’.', 1),
    ('The verb form ‘differ’ does not seem to match the subject ‘balance’.', 1),
    ('The verb form ‘differ’ does not seem to match the subject ‘force’.', 1),
    ('The verb form ‘differ’ does not seem to match the subject ‘student’.', 1),
    ('The verb form ‘differ’ does not seem to match the subject ‘birth’.', 1),
    ('The verb form ‘differ’ does not seem to match the subject ‘yield’.', 1),
    ('The verb form ‘differ’ does not seem to match the subject ‘debt’.', 1),
    ('The verb form ‘is’ does not seem to match the subject ‘flows’.', 1),
    ('The verb form ‘is’ does not seem to match the subject ‘subscribers’.', 1)]
    """


def fix_one_plural(doc, nlp):
    if not isinstance(doc, Doc):
        doc = nlp(doc)
    orgdoc = doc.copy()
    edits = []
    words = [t.text for t in orgdoc]
    spaces = [bool(t.whitespace_) for t in doc]
    # Find noun chunks

    for chunk in orgdoc.noun_chunks:
        if len(chunk) != 2:
            continue
        (cd, noun), tags = zip(*[(t, t.tag_) for t in chunk])
        # If it is of the form "1 plural_form",
        if tags == ('CD', 'NNS'):
            cd, noun = chunk
            if cd.text == '1':
                singular_noun = noun.lemma_
                edits.append((noun.text, singular_noun))
                new_chunk = cd.text, singular_noun
                words[chunk.start:chunk.end] = new_chunk
                doc = Doc(orgdoc.vocab, words=words, spaces=spaces)
    return doc, edits


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
    import pandas as pd

    with open("data/strat_sample.json", "r") as fin:
        data = json.load(fin)

    res = Parallel(n_jobs=-1, verbose=2)(delayed(process)(**r) for r in data)

    df = pd.DataFrame.from_records(data).set_index("question_id", verify_integrity=True)
    res = (
        pd.DataFrame.from_records(res)
        .set_index("question_id", verify_integrity=True)
        .squeeze("columns")
    )
    df["matches"] = res
    df.reset_index().to_json('data/strat_sample.json', orient='records', indent=2)
