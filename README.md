# The Lean Machine Learning library site

**Site:** https://leanmachinelearning.org/library/

What is formalized in Lean Machine Learning, to discover in words and to review: the human-reviewed
core [LML](https://github.com/LeanMachineLearning/LML), the AI-written
[LMLExplore](https://github.com/LeanMachineLearning/LMLExplore), and
[Statlib](https://github.com/stat-lib/statlib), which LML builds on. Every page says which library a
result comes from; a result's page takes its statement apart, shows what it rests on by library and
who has reviewed it, and asks whether it is correctly stated.

It is built with the [LeanTrustBuilders](https://github.com/LeanTrustBuilders) tools: the three
libraries extracted as one dataset (the extractor, with three roots), the evidence stores
[LMLExplore-evidence](https://github.com/LeanMachineLearning/LMLExplore-evidence) and
[LML-evidence](https://github.com/LeanMachineLearning/LML-evidence) (Statlib's declarations are
reviewed in LML's), and `referee-site library`.

## What is here

| file | what it is |
|---|---|
| `site.toml` | the site: its libraries (each with its store and how it is written), navigation, sections, how to contribute |
| `topics.toml` | which folders of which library make up each topic; titles and summaries are shown as written |
| `scripts/roadmaps.py` | the roadmaps of [LMLRoadmaps](https://github.com/LeanMachineLearning/LMLRoadmaps) as the plans the site reads |
| `.github/workflows/site.yml` | the build: twice a day after LMLExplore's dataset, and every hour when a review was filed |

The literature comes from LMLExplore's `scripts/literature/annotations.py`, run on the three
libraries' dataset, and the papers from the `papers.json` LMLExplore's site publishes.

## Reviewing

On a declaration's page, **Yes** and **No** open a short form in the store of its library, filled in
for that declaration; intake records the answer under the account that filed it, and the site shows
it within the hour. **Copy instructions for your AI** gives an agent what it needs to review from the
command line.

## Building it locally

```bash
pip install "referee-site @ git+https://github.com/LeanTrustBuilders/referee-site@v0.14.3"
python3 scripts/roadmaps.py --roadmaps path/to/LMLRoadmaps --out plans.json
referee-site library --config site.toml --dataset DATASET --source path/to/LMLExplore --out site/ \
  --evidence path/to/LMLExplore-evidence/evidence --imports IMPORTS \
  --literature annotations.jsonl --papers papers.json --plans plans.json
```

`DATASET` is a release of this repository (`dataset-<commit12>`), and `IMPORTS` what
`evidence-store fetch-imports` writes. `#/check` on the site lists what the topics file, the
literature and the papers say that the dataset does not bear out.
