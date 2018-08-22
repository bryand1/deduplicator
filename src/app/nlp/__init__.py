from typing import List

from .ner import NER
from .stopwords import stopwords


class Tokenizer:

    def tokenize(self, s: str) -> List[str]:
        # Iterate through the string and break on whitespace, unless within quotes
        tokens = self._tokenize(s)
        return list(filter(lambda x: x not in stopwords, map(self._lowercase, tokens)))

    @staticmethod
    def _lowercase(s: str) -> str:
        _openquote = {'"', "'", "“", "‘"}
        return s if s[0] in _openquote else s.lower()

    @staticmethod
    def _tokenize(s: str) -> List[str]:
        return s.split()
