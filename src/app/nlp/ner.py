import spacy

from app import util


class NER:

    logger = util.get_logger("nlp.ner.NER")

    def __init__(self):
        self.logger.debug("Loading spaCy")
        self.nlp = spacy.load('en_core_web_lg')

    def doc(self, expr):
        return self.nlp(expr)

    @staticmethod
    def entities(doc):
        return set(map(lambda x: x.text, filter(lambda x: x.label_ in {'NORP', 'LOC', 'GPE'}, doc.ents)))
