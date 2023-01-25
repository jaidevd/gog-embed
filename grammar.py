import json
from collections import Counter
from requests import get
import gc
import re
from joblib import Parallel, delayed
from tqdm import tqdm
from spacy.tokens import Doc
import pandas as pd


URL = "http://localhost:8081/v2/check"
AUX_VERB_PLURALIZE = {
    "was": "were",
    "is": "are",
    "does": "do",
    "has": "have",
    "differs": "differ",
}
AUX_VERB_SINGULARIZE = {v: k for k, v in AUX_VERB_PLURALIZE.items()}
is_noun_singular = lambda x: x.tag_ in ("NN", "NNP")  # NOQA: E731
is_noun_plural = lambda x: x.tag_ in ("NNS", "NNPS")  # NOQA: E731


def process(question_id, caption, template_id=None, **kwargs):
    resp = get(URL, params={"language": "en-US", "text": caption})
    if resp.ok:
        return {"question_id": question_id, "matches": resp.json()["matches"]}
    raise ValueError(f"LT Request failed with status {resp.status_code}")


def has_match(matches, key, value):
    for match in matches:
        if value.lower() in match[key].lower():
            return True
    return False


def err_counter(messages):
    msgs = []
    for m in messages:
        for match in m['matches']:
            msgs.append(match['message'])
    return Counter(msgs)


def filter_lt_messages(messages, reverse=False, **kwargs):
    if all([k is None for k in kwargs.values()]):
        raise ValueError('At least one kwarg must be ~None.')
    for k, v in kwargs.items():
        if reverse:
            messages = filter(lambda x: not has_match(x['matches'], k, v), messages)
        else:
            messages = filter(lambda x: has_match(x['matches'], k, v), messages)
    return [m for m in messages if len(m['matches']) > 0]


# Fixes


def find_root_nsubj(doc):
    root = None
    for token in doc:
        if token.dep_ == "ROOT":
            root = token
            break
    if root is None:
        raise ValueError("Cannot find root!")
    aux_verb = None
    for child in root.children:
        if child.dep_ == "aux":
            aux_verb = child
    nsubj = None
    for noun in root.children:
        if noun.dep_ == "nsubj":
            nsubj = noun
            if nsubj.pos_ == "ADJ":
                nsubj = nsubj.conjuncts[0]
            break
    if (aux_verb is not None) and (nsubj in aux_verb.children):
        root = aux_verb
    return root, nsubj


def has_agreement(verb, subject):
    if (subject is None) or (subject.tag_ == "CD"):
        return True, verb

    if verb.tag_ == "VBP":
        return is_noun_plural(subject), verb
    if verb.tag_ == "VBZ":
        return is_noun_singular(subject), verb
    if verb.tag_ == "VBD":
        is_singular = verb.morph.get("Number") == ["Sing"]
        if is_singular:
            return is_noun_singular(subject), verb
        return is_noun_plural(subject), verb
    if verb.tag_ == "VB":
        # Find the auxiliary child and that becomes the new verb
        for child in verb.children:
            if child.dep_ == "aux":
                break
        return has_agreement(child, subject)
    raise ValueError(f"Tag for verb {verb} not valid.")


def fix_verb_subject_agreement(doc):
    verb, subject = find_root_nsubj(doc)
    agrees, verb = has_agreement(verb, subject)
    verbix = verb.i
    if agrees:
        return doc
    if subject.tag_ in ("NN", "NNP"):  # subject is singular
        verb = AUX_VERB_SINGULARIZE[verb.text]
    elif subject.tag_ in ("NNS", "NNPS"):  # subject is plural
        verb = AUX_VERB_PLURALIZE.get(verb.text, verb.lemma_)
    elif subject.tag_ in ("NFP",):
        return doc
    else:
        raise ValueError(f"Tag {subject.tag_} of noun {subject.text} not recognized.")
    words = [t.text for t in doc]
    words[verbix] = verb
    spaces = [bool(t.whitespace_) for t in doc]
    return Doc(doc.vocab, words, spaces).text


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
    return re.sub(r"(?P<prefix>\S)\(", r"\g<prefix> (", s)


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
    return re.sub(r"(?P<nnp>.*), The", r"The \g<nnp>", s)


def unpaired_symbol(s, sym):
    count = s.count(sym)
    if count > 0 and s.count(sym) % 2 == 0:
        msg = f"Symbol {sym} is not unpaired in the sentence:\n" + s
        raise ValueError(msg)
    raise NotImplementedError


def trim_leading_symbols(s, sym='"'):
    count = s.count(sym)
    if count > 0 and s.count(sym) % 2 == 0:
        msg = f"Symbol {sym} is not unpaired in the sentence:\n" + s
        raise ValueError(msg)
    return re.sub(f"^\\s*{sym}\\s*", "", s)


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


def fix_determiner_superlative(doc):
    """                      the
    The highest population in   largest city across years is 200.
                              ^ -------
                              (superlative)
    """
    # If an adjective is superlative:
    # If an adjective has a determiner, leave it alone.
    # It it's conjunct noun has a determiner, leave it alone.
    # If it has no determiner, but it's ancestor noun (to which the adj is amod) has one,
    # leave it alone.
    # otherwise add a determiner if it is supelative.


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
        if tags == ("CD", "NNS"):
            cd, noun = chunk
            if cd.text == "1":
                singular_noun = noun.lemma_
                edits.append((noun.text, singular_noun))
                new_chunk = cd.text, singular_noun
                words[chunk.start: chunk.end] = new_chunk
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


def draw_sample(path='data/qa_captions.json', size=10_000):
    samples = []
    for i, df in tqdm(
        enumerate(
            pd.read_json("data/qa_captions.json", lines=True, chunksize=1_000_000)
        )
    ):
        xdf = df.sample(10_000)
        res = Parallel(n_jobs=-1, verbose=2)(delayed(process)(**r) for _, r in xdf.iterrows())
        res = [c for c in res if len(c['matches']) > 0]
        samples.extend(res)
    return samples


if __name__ == "__main__":
    samples = draw_sample()
    typos = filter_lt_messages(samples, message='Possible spelling mistake')
    typos = filter_lt_messages(samples, reverse=True, message='British English')
    T = []
    for t in typos:
        for match in t['matches']:
            sentence = match['sentence']
            if match['message'].startswith('Possible spelling mistake'):
                start = match['offset']
                end = start + match['length']
                s = sentence[start:end]
                T.append(s)
    print(set(T))
