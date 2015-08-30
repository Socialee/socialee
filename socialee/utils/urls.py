import six.moves.urllib_parse as urlparse


def is_absolute_url(url):
    return bool(urlparse.urlparse(url).netloc)


def make_absolute_url(url, base, default_scheme='http'):
    parsed = urlparse.urlparse(url)
    if parsed.netloc:
        if not parsed.scheme:
            assert url.startswith('//')
            url = default_scheme + ':' + url
        return url
    if base.endswith('/') and url.startswith('/'):
        url = url[1:]
    return base + url


def url_with_querystring(path, **kwargs):
    assert '?' not in path
    return path + '?' + urlparse.urlencode(kwargs)

