# Tal & Florentin (2024) vs CACCHT SP

Scripts that compare the Hebrew running text of Moshe Florentin and Abraham Tal, *The Samaritan
Pentateuch: An English Translation with a Parallel Annotated Hebrew Text* (Open Book Publishers 2024,
https://doi.org/10.11647/OBP.0415, CC BY-NC 4.0) with the CACCHT dataset. T&F print MS Nablus 6,
CACCHT MS Dublin CBL 751 (+ MS Garizim 1 for Deut 32:36b–34).

The differences are added to the dataset as variant features by `scripts/make_7_5_0.py`
(`var_ft_utf8`, `var_ft`, `var_ft_type`, `var_ft_span`, `verse_ft`; see the docs). The CACCHT text
itself is not changed. `tests/test_tal_florentin.py` checks that CACCHT + these features gives back
exactly the T&F text of `results/tf_verses.json`.

Files:
- `extract_tf.py`: Hebrew running text of T&F from the PDF (by font and character position)
- `extract_caccht.py`: graphic words of a CACCHT data version, with their word nodes
- `compare.py`: per-chapter alignment and classification
- `results/differences.md`: report of all differences (versions, nodes, types, both texts)
- `results/differences.tsv`: the same as a table; this is the input of `make_7_5_0.py`
- `results/versification.tsv`: CACCHT verses whose words stand under another verse number in T&F
- `results/tf_verses*.json`, `results/caccht_verses*.json`: extracted texts, T&F pages, CACCHT nodes, metadata

Reproduce (from this folder; the PDF is not in the repository, download it via the DOI and save it
here as `tal_florentin_SP.pdf`; check its SHA-256 against `results/differences.md`):

    pip install pymupdf text-fabric
    python extract_tf.py tal_florentin_SP.pdf results/tf_verses.json
    python extract_caccht.py ../../tf/7.4.1 results/caccht_verses.json
    python compare.py results/tf_verses.json results/caccht_verses.json results

The node numbers in `results/` belong to data version 7.4.1. If the slots change in a later version
(e.g. a text repair or a change in segmentation), rerun `extract_caccht.py` and `compare.py` against the old
version and carry the variant features over in the build script of the new version.
