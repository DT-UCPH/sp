# The Samaritan Pentateuch

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7734632.svg)](https://doi.org/10.5281/zenodo.7734632) [![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

In this repo you find our Text-Fabric dataset of the Samaritan Pentateuch.
The dataset is work in progress, and so far, we have added a number of word features, which you find in the tf folder. The features are similar to those of the Biblia Hebraica Stuttgartensia Amstelodamensis (BHSA), so we refer to the [BHSA feature documentation](https://etcbc.github.io/bhsa/) for more explanation of the features.

The text was provided by the Samaritanus-project based at Martin-Luther-Universität Halle-Wittenberg, directed by Stefan Schorch, and is based on a transcription MS Dublin Chester Beatty Library 751 (Gen 1-Deut 32:36) + MS Garizim 1 (Deut 32:36b-34), cf. Stefan Schorch (ed.), The Samaritan Pentateuch: A critical editio maior. Berlin: de Gruyter, 2018-.

We have made a small change in the original verse division. Instead of assigning the additions after Genesis 30:36 to the verse numbers 36a, 36b, and 36 c, we group these under verse 36.

Here and there we still need to decide which value a feature should have for a specific object. In this case, the value is "absent".

### Versions

This repo is work in progress. Before version 2.0, the dataset consisted of the text of Genesis. In 2.0 the text of the other four books was added. This started with the feature g_cons_raw. Other features are implemented gradually. If a feature has not been implemented yet for those books, the values are '?'.

Version
- 0.1 9. November 2022 First data of the book of Genesis.
- 1.0 29. December 2022
- 2.0 23. February 2023 Addition of g_cons_raw of Exodus-Deuteronomy.

The features were first added for the book of Genesis. Presently, we are adding the annotations for the other four books. Features that are added for all five books are:
- g_cons
- lex
- sp
- g_vbs
- g_pfm
- g_lex
- g_vbe
- g_nme
