from difflib import SequenceMatcher

from app import util


class Deduplicator:

    logger = util.get_logger("deduplicator.Deduplicator")
    threshold = 0.35

    def __init__(self):
        self.sm = SequenceMatcher()
        self.headlines = dict()
        self.parents = dict()
        self.groups = set()

    def accept(self, _id: str, headline: str) -> str:
        self.headlines[_id] = headline

        if len(self.groups) == 0:
            self.logger.debug("[%s] %s - first item", _id, headline)
            self.parents[_id] = _id
            self.groups.add(_id)
            return _id

        matches = []
        a = headline
        for group_id in self.groups:
            b = self.headlines[group_id]
            self.sm.set_seqs(a, b)
            ratio = self.sm.ratio()
            self.logger.debug("[%s] %s <-> [%s] %s ==> %.2f", _id, a, group_id, b, ratio)
            if ratio > self.threshold:
                matches.append((ratio, group_id))

        if not matches:
            self.logger.debug("[%s] %s - no matches found", _id, headline)
            self.parents[_id] = _id
            self.groups.add(_id)
            return _id

        matches.sort(key=lambda x: x[0])
        highest_ratio, group_id = matches.pop()
        b = self.headlines[group_id]
        self.logger.debug("[%s] %s <-> [%s] %s ==> %.2f was the high score", _id, a, group_id, b, highest_ratio)
        self.parents[_id] = group_id
        return group_id
