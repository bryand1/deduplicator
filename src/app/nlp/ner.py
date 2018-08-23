import spacy

from app import util
from .norp import norp_gpe_map


class NER:

    logger = util.get_logger("nlp.ner.NER")

    def __init__(self, model='en_core_web_lg'):
        self._model = model
        self.logger.debug("Loading spaCy %s", self._model)
        self.nlp = spacy.load(self._model)

    def doc(self, expr):
        return self.nlp(expr)

    @staticmethod
    def _ent_to_text(ent):
        if ent.label_ == 'NORP':
            return norp_gpe_map.get(ent.text, ent.text)
        else:
            return ent.text

    def entities(self, doc):
        return set(map(self._ent_to_text, filter(lambda x: x.label_ in {'NORP', 'LOC', 'GPE'}, doc.ents)))
