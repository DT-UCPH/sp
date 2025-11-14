Doc4TF pages for [The Samaritan Pentateuch](https://github.com/DT-UCPH/sp/tree/master/tf) (version 5.0.2)
# Overview features by node type
Overview by [name](featuresbyname.md), [data type](featuresbydatatype.md), or [feature type](featuresbytype.md).
## book

Feature|Feature type|Data type|Description|Examples
---|---|---|---|---
[`book`](book.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|book title|`Deuteronomy` `Exodus` `Genesis` `Leviticus`
## chapter

Feature|Feature type|Data type|Description|Examples
---|---|---|---|---
[`chapter`](chapter.md#readme)|[`Node`](featuresbytype.md#Node)|[`Integer`](featuresbydatatype.md#Integer)|chapter number|`1` `2` `3` `4`
## verse

Feature|Feature type|Data type|Description|Examples
---|---|---|---|---
[`verse`](verse.md#readme)|[`Node`](featuresbytype.md#Node)|[`Integer`](featuresbydatatype.md#Integer)|verse number|`1` `4` `5` `6`
## phrase

Feature|Feature type|Data type|Description|Examples
---|---|---|---|---
## phrase atom

Feature|Feature type|Data type|Description|Examples
---|---|---|---|---
## word

Feature|Feature type|Data type|Description|Examples
---|---|---|---|---
[`ETCBC_parsing`](ETCBC_parsing.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|Word parsing in ETCBC-format|`W` `H` `L` `B`
[`g_cons`](g_cons.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|word consonantal-transliterated|`W` `H` `L` `>T`
[`g_cons_raw`](g_cons_raw.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|word consonantal-transliterated (without disambiguation of Shin (C) and Sin (F))|`W` `H` `L` `>T`
[`g_cons_utf8`](g_cons_utf8.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|word in Hebrew script|`ו` `ה` `ל` `את`
[`g_lex`](g_lex.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized lexeme|`W` `H` `L` `>T`
[`g_lex_utf8`](g_lex_utf8.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized lexeme in Hebrew script|`ו` `ה` `ל` `את`
[`g_nme`](g_nme.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized nominal ending consonantal|`` `/` `/J` `/JM`
[`g_nme_utf8`](g_nme_utf8.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized nominal ending consonantal in Hebrew script|`/` `/י` `/ים` `/ת`
[`g_pfm`](g_pfm.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized verbal preformative consonantal|`` `!J!` `!!` `!T!`
[`g_pfm_utf8`](g_pfm_utf8.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized verbal preformative consonantal in Hebrew script|`!י!` `!!` `!ת!` `!א!`
[`g_prs`](g_prs.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized pronominal suffix consonantal|`` `+W` `+K` `+KM`
[`g_prs_utf8`](g_prs_utf8.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized pronominal suffix consonantal in Hebrew script|`+ו` `+ך` `+כם` `+ם`
[`g_uvf`](g_uvf.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized univalent final|`` `~J` `~H` `~N`
[`g_uvf_utf8`](g_uvf_utf8.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized univalent final in Hebrew script|`~י` `~ה` `~ן` `~`
[`g_vbe`](g_vbe.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized verbal ending consonantal|`` `[` `[W` `[T`
[`g_vbe_utf8`](g_vbe_utf8.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized verbal ending consonantal in Hebrew script|`[` `[ו` `[ת` `[תי`
[`g_vbs`](g_vbs.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized verbal stem consonantal|`` `]]` `]H]` `]N]`
[`g_vbs_utf8`](g_vbs_utf8.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|realized verbal stem consonantal in Hebrew script|`]]` `]ה]` `]נ]` `]ת]`
[`gn`](gn.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|gender|`NA` `m` `unknown` `f`
[`language`](language.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|language|`Hebrew`
[`lex`](lex.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|lexeme consonantal-transliterated|`W` `H` `L` `>T`
[`lex_utf8`](lex_utf8.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|lexeme in Hebrew script|`ו` `ה` `ל` `את`
[`mt_feat`](mt_feat.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|features imposed from MT|`True` ``
[`node`](node.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|word node|`405426` `405427` `405428` `405429`
[`nu`](nu.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|grammatical number|`NA` `sg` `pl` `unknown`
[`prediction`](prediction.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|neural network prediction|`W` `H` `L` `Wn`
[`prs_gn`](prs_gn.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|pronominal suffix gender|`NA` `m` `unknown` `f`
[`prs_nu`](prs_nu.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|pronominal suffix number|`NA` `sg` `pl`
[`prs_ps`](prs_ps.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|pronominal suffix person|`NA` `p3` `p2` `p1`
[`ps`](ps.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|grammatical person|`NA` `p3` `unknown` `p2`
[`sp`](sp.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|part of speech|`subs` `prep` `verb` `conj`
[`trailer`](trailer.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|interword material|` ` ``
[`vt`](vt.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|verbal tense|`NA` `impf` `perf` `infc`
## sign

Feature|Feature type|Data type|Description|Examples
---|---|---|---|---
[`sign`](sign.md#readme)|[`Node`](featuresbytype.md#Node)|[`String`](featuresbydatatype.md#String)|consonantal letter|` ` `י` `ו` `ה`


Created on Nov. 14, 2025 using [Doc4TF version 0.5.2 (July 10, 2024)](https://github.com/tonyjurg/Doc4TF/blob/main/CreateFeatureDoc.ipynb)