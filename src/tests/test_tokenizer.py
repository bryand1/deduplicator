from app.tokenizer import Tokenizer

tokenizer = Tokenizer()


def test_lowercase():
    assert tokenizer._lowercase("Facebook") == "facebook"
    assert tokenizer._lowercase("'Fake News'") == "'Fake News'"


def test_headlines():
    headline = "Facebook seeks outside help as part of latest fake account purge"
    tokens = tokenizer.tokenize(headline)
    assert tokens == ['facebook', 'seeks', 'outside', 'help', 'part', 'latest', 'fake', 'account', 'purge']
