Doc4TF pages for [The Samaritan Pentateuch](https://github.com/DT-UCPH/sp/tree/master/tf) (version 5.0.2)
# Overview features by data type
Overview by [name](featuresbyname.md), [node type](featuresbynodetype.md), or [feature type](featuresbytype.md).
## Integer

Feature|Featuretype|Available on nodes|Description|Examples
---|---|---|---|---
[`chapter`](chapter.md#readme)|[`Node`](featuresbytype.md#node)|[`chapter`](featuresbynodetype.md#chapter) |chapter number|`1` `2` `3` `4`
[`verse`](verse.md#readme)|[`Node`](featuresbytype.md#node)|[`verse`](featuresbynodetype.md#verse) |verse number|`1` `4` `5` `6`

## String

Feature|Featuretype|Available on nodes|Description|Examples
---|---|---|---|---
[`ETCBC_parsing`](ETCBC_parsing.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |Word parsing in ETCBC-format|`W` `H` `L` `B`
[`book`](book.md#readme)|[`Node`](featuresbytype.md#node)|[`book`](featuresbynodetype.md#book) |book title|`Deuteronomy` `Exodus` `Genesis` `Leviticus`
[`g_cons`](g_cons.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |word consonantal-transliterated|`W` `H` `L` `>T`
[`g_cons_raw`](g_cons_raw.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |word consonantal-transliterated (without disambiguation of Shin (C) and Sin (F))|`W` `H` `L` `>T`
[`g_cons_utf8`](g_cons_utf8.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |word in Hebrew script|`ו` `ה` `ל` `את`
[`g_lex`](g_lex.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized lexeme|`W` `H` `L` `>T`
[`g_lex_utf8`](g_lex_utf8.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized lexeme in Hebrew script|`ו` `ה` `ל` `את`
[`g_nme`](g_nme.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized nominal ending consonantal|`` `/` `/J` `/JM`
[`g_nme_utf8`](g_nme_utf8.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized nominal ending consonantal in Hebrew script|`/` `/י` `/ים` `/ת`
[`g_pfm`](g_pfm.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized verbal preformative consonantal|`` `!J!` `!!` `!T!`
[`g_pfm_utf8`](g_pfm_utf8.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized verbal preformative consonantal in Hebrew script|`!י!` `!!` `!ת!` `!א!`
[`g_prs`](g_prs.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized pronominal suffix consonantal|`` `+W` `+K` `+KM`
[`g_prs_utf8`](g_prs_utf8.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized pronominal suffix consonantal in Hebrew script|`+ו` `+ך` `+כם` `+ם`
[`g_uvf`](g_uvf.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized univalent final|`` `~J` `~H` `~N`
[`g_uvf_utf8`](g_uvf_utf8.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized univalent final in Hebrew script|`~י` `~ה` `~ן` `~`
[`g_vbe`](g_vbe.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized verbal ending consonantal|`` `[` `[W` `[T`
[`g_vbe_utf8`](g_vbe_utf8.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized verbal ending consonantal in Hebrew script|`[` `[ו` `[ת` `[תי`
[`g_vbs`](g_vbs.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized verbal stem consonantal|`` `]]` `]H]` `]N]`
[`g_vbs_utf8`](g_vbs_utf8.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |realized verbal stem consonantal in Hebrew script|`]]` `]ה]` `]נ]` `]ת]`
[`gn`](gn.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |gender|`NA` `m` `unknown` `f`
[`language`](language.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |language|`Hebrew`
[`lex`](lex.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |lexeme consonantal-transliterated|`W` `H` `L` `>T`
[`lex_utf8`](lex_utf8.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |lexeme in Hebrew script|`ו` `ה` `ל` `את`
[`mt_feat`](mt_feat.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |features imposed from MT|`True` ``
[`node`](node.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |word node|`405426` `405427` `405428` `405429`
[`nu`](nu.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |grammatical number|`NA` `sg` `pl` `unknown`
[`oslots`](oslots.md#readme)|[`Edge`](featuresbytype.md#edge)||No feature description|No values
[`otype`](otype.md#readme)|[`Node`](featuresbytype.md#node)||No feature description|No values
[`prediction`](prediction.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |neural network prediction|`W` `H` `L` `Wn`
[`prs_gn`](prs_gn.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |pronominal suffix gender|`NA` `m` `unknown` `f`
[`prs_nu`](prs_nu.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |pronominal suffix number|`NA` `sg` `pl`
[`prs_ps`](prs_ps.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |pronominal suffix person|`NA` `p3` `p2` `p1`
[`ps`](ps.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |grammatical person|`NA` `p3` `unknown` `p2`
[`sign`](sign.md#readme)|[`Node`](featuresbytype.md#node)|[`sign`](featuresbynodetype.md#sign) |consonantal letter|` ` `י` `ו` `ה`
[`sp`](sp.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |part of speech|`subs` `prep` `verb` `conj`
[`trailer`](trailer.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |interword material|` ` ``
[`vt`](vt.md#readme)|[`Node`](featuresbytype.md#node)|[`word`](featuresbynodetype.md#word) |verbal tense|`NA` `impf` `perf` `infc`


Created on Nov. 14, 2025 using [Doc4TF version 0.5.2 (July 10, 2024)](https://github.com/tonyjurg/Doc4TF/blob/main/CreateFeatureDoc.ipynb)