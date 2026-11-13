# Feature: var_ft_utf8
Data type|Feature type|Available for nodes
---|---|---
[`String`](featuresbydatatype.md#string)|[`Node`](featuresbytype.md#node)| [`word`](featuresbynodetype.md#word) 
## Description
Reading of the Tal & Florentin edition where it differs from this text, in Hebrew script; `-` = T&F have no words here. Example: Gen 1:12 ותוצא, T&F ותוציא.

The Tal & Florentin (T&F) edition prints the Hebrew text of MS Nablus 6 (1204 CE), with gaps filled from other manuscripts. The text of this dataset (MS Dublin CBL 751 + MS Garizim 1) is not changed; where T&F read differently, their reading is added to the word nodes with the features [`var_ft_utf8`](var_ft_utf8.md), [`var_ft`](var_ft.md), [`var_ft_type`](var_ft_type.md) and [`var_ft_span`](var_ft_span.md). Verses that T&F number differently get [`verse_ft`](verse_ft.md).

How a variant is encoded: the features stand on the **first** word node of the differing stretch. `var_ft_span` gives the number of word nodes (from that node on) that the T&F reading replaces. `var_ft_span` = 0 means that T&F have extra words after this word; `var_ft_utf8` = `-` means that T&F have no words for the stretch. Because prefixes such as ו, ה and ב are separate word nodes here, a stretch always consists of whole graphic words; the reading of a compound name (one word node, e.g. באר לחי ראה) is given for the whole name.

The comparison was made with `scripts/tal_florentin` (graphic words aligned per chapter; see the README there). The four scribal colophons at the end of Exodus–Deuteronomy in T&F are not included. Source: [Florentin & Tal 2024](https://doi.org/10.11647/OBP.0415) (Open Book Publishers, CC BY-NC 4.0). Added in version 7.5.0.

## Feature Values
### Frequency for nodetype [word](featuresbynodetype.md#word)
Value|Occurences
---|---
אבותיך|17
לדורתיכם|13
תהיינה|12
חקת|12
היושבים|10
אבותיכם|9
הסהר|8
חקתי|8
לאבותיך|8
את|7

Total frequency of feature: 1074. (10 most frequent of 754 values shown.)
