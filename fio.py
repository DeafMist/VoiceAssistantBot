from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,
    AddrExtractor,

    Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)
addr_extractor = AddrExtractor(morph_vocab)


def get_fio(text: str):
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)

    for span in doc.spans:
        span.normalize(morph_vocab)

    for span in doc.spans:
        if span.type == PER:
            span.extract_fact(names_extractor)

    names_dict = {_.normal: _.fact.as_dict for _ in doc.spans if _.fact}

    if names_dict == {}:
        return None

    res = ["", ""]

    for name, fio in names_dict.items():
        if fio.get("last") is not None:
            res[0] = fio.get("last")
        if fio.get("first") is not None:
            res[1] = fio.get("first")

        return res
