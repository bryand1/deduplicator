from difflib import SequenceMatcher

from app.nlp import NER, Tokenizer
from app import util


class Deduplicator:

    logger = util.get_logger("deduplicator.Deduplicator")
    threshold = 0.50
    boost = 0.10

    def __init__(self):
        self.sm = SequenceMatcher()
        self.tokenizer = Tokenizer()
        self.ner = NER()
        self.headlines = dict()
        self._headlines = dict()
        self.parents = dict()
        self.groups = dict()

    def accept(self, _id: str, headline: str) -> str:
        self.headlines[_id] = headline
        tokens = self.tokenizer.tokenize(headline)
        _headline = ' '.join(tokens)
        self._headlines[_id] = _headline

        if len(self.groups) == 0:
            self.logger.debug("[%s] %s - first item", _id, headline)
            self.parents[_id] = _id
            self.groups[_id] = []
            return _id

        matches = []
        a = _headline
        doc1 = self.ner.doc(headline)
        ents1 = util.lowercase(self.ner.entities(doc1))
        for group_id in self.groups:
            b = self._headlines[group_id]
            self.sm.set_seqs(a, b)
            ratio = self.sm.ratio()
            # Check if there are any named entities in common
            doc2 = self.ner.doc(self.headlines[group_id])
            ents2 = util.lowercase(self.ner.entities(doc2))
            ncommon = len(set(ents1) & set(ents2))
            boost = ncommon * self.boost
            ratio += boost
            self.logger.debug("[%s] %s <-> [%s] %s ==> %.2f (+%.2f)", _id, a, group_id, b, ratio, boost)
            if ratio >= self.threshold:
                matches.append((ratio, group_id))

        if not matches:
            self.logger.debug("[%s] %s - no matches found", _id, headline)
            self.parents[_id] = _id
            self.groups[_id] = []
            return _id

        matches.sort(key=lambda x: x[0])
        highest_ratio, group_id = matches.pop()
        b = self._headlines[group_id]
        self.logger.debug("[%s] %s <-> [%s] %s ==> %.2f was the high score", _id, a, group_id, b, highest_ratio)
        self.parents[_id] = group_id
        self.groups[group_id].append(_id)
        return group_id

    def print_tree(self, original=True):
        headlines = self.headlines if original else self._headlines
        print("")
        for group_id in self.groups:
            print("[%s] %s" % (group_id, headlines[group_id]))
            if self.groups[group_id]:
                print(" |")
            for _id in self.groups[group_id]:
                print(" |-- [%s] %s" % (_id, headlines[_id]))
            if self.groups[group_id]:
                print("")
        print("")

    def export(self):
        return {
            'headlines': self.headlines,
            '_headlines': self._headlines,
            'parents': self.parents,
            'groups': self.groups
        }
