from urllib.parse import urlparse

def is_url_valid(url: str) -> bool:
    try:
        result = urlparse(url)
        return all((result.scheme, result.netloc))
    except AttributeError:
        return False
    