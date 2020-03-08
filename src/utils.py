from urllib import parse


def remove_whitespace(string):
    return " ".join(string.split())


def encode_to_url(string):
    return parse.quote(string)


def decode_url(url):
    return parse.unquote_plus(url)
