# PlotCaptions

The task proposed by the [PlotQA paper](https://arxiv.org/pdf/1909.00997.pdf)
was that of training a machine to answer questions based on a scientific plot.
The proposed 'sentencification' of QA pairs allows us to train machines to
generate captions for plots.

This repository contains code to generate a variant of the [PlotQA](https://github.com/NiteshMethani/PlotQA/blob/master/PlotQA_Dataset.md) dataset, which converts the QA pairs in the
original dataset to sentences. Here is a sample QA pair from the original
dataset:

Question: Across all years, what is the maximum percentage of male population who survived till age of 65?
Answer: 82.0172

This QA pair can be presented as a sentence, as follows:

Across years, the maximum percentage of male population who survived till the
age of 65  is 82.0172.


## Question templates

The original paper helpfully provides a collection of templates that were used
to generate questions which were eventually included in the original dataset. A
generalization of these templates is included [here](./qa_templates.yaml).

Such templates can then be used to convert the question answer pair into a
sentence.

Consider the following question:

```
What is the percentage of female population who survived till age of 65 in 1993?
```

This string is matched by the second template in our list:

```
"What is the (?P<yvalue>.*?) (?P<preposition>of|in) (?P<xvalue>.*?)\\s?\\?$"
```

This can be done in Python as follows:

```python
>>> import re
>>> question = "What is the percentage of female population who survived till age of 65 in 1993?"
>>> pattern = "What is the (?P<yvalue>.*?) (?P<preposition>of|in) (?P<xvalue>.*?)\\s?\\?$"
>>> matches = re.search(pattern, question).groupdict()
>>> print(matches)
{'yvalue': 'percentage',
 'preposition': 'of',
 'xvalue': 'female population who survived till age of 65 in 1993'}
```

## Caption Generation

From the training data, we know the answer to be 87.4244. So, this can then be templatized into an answer as follows:

```python
>>> answer_template = "The {yvalue} {preposition} {xvalue} is {answer}."
>>> print(answer_template.format(answer=87.4244, **matches))
The percentage of female population who survived till age of 65 in 1993 is 87.4244.
```

The QA templates have been written so as to randomize the answer templates, i.e.
for all question matching this pattern, the caption template will not
necessarily be the same as `answer_template` above.

## Usage

Suppose you have a QA pair from the original data as follows:

```python
>>> qa_sample = {
...     "question_string": "What is the percentage of female population who survived till age of 65 in 1993 ?",
...     "answer": 87.4244,
...     "question_id": 2
... }
```

Then, the right template can be found as follows:
```python
>>> # Read the templates into memory
>>> import yaml
>>> from plotqa import search_templates
>>> with open("qa_templates.yaml", "r") as fin:
...     tmpl_cfg = pd.DataFrame.from_records(yaml.safe_load(fin), index="id")
...     templates = tmpl_cfg['regex'].reset_index().to_dict(orient='records')
>>> matched_template = search_templates(tmpl_cfg, **qa_sample)
>>> print(matched_template)
{'question_id': 2,
 'template_id': 2,
 'matches': {'yvalue': 'percentage',
             'preposition': 'of',
	     'xvalue': 'female population who survived till age of 65 in 1993'}}
>>> # This means that the given QA pair matched template ID 2
```

The caption can then be generated as:
```python
>>> from plotqa import caption_qa
>>> caption = caption_qa(answer=qa_sample['answer'], **matched_template)
>>> print(caption)
{'question_id': 2,
 'template_id': 2,
 'caption': ' The percentage of female population who survived till age of 65 in 1993 is 87.4244. '}
 ```
