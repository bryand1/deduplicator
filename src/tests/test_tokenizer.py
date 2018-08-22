from app.nlp import NER, Tokenizer
from app.util import lowercase

tokenizer = Tokenizer()
ner = NER()


def test_lowercase():
    assert tokenizer._lowercase("Facebook") == "facebook"
    assert tokenizer._lowercase("'Fake News'") == "'Fake News'"


def test_headlines():
    headline = "Facebook seeks outside help as part of latest fake account purge"
    tokens = tokenizer.tokenize(headline)
    assert tokens == ['facebook', 'seeks', 'outside', 'help', 'part', 'latest', 'fake', 'account', 'purge']


def test_ner():
    doc1 = ner.doc("Facebook and Twitter dismantle disinformation campaigns tied to Iran and Russia")
    ent1 = ner.entities(doc1)
    assert ent1 == {'Iran', 'Russia'}
    assert lowercase(ent1) == {'iran', 'russia'}
