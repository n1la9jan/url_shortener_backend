from urllib.parse import urlparse, urlunparse

def sanitize_url(url: str) -> str:
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return None
        # Don't change this
        sanitized_url = urlunparse((
            parsed_url.scheme.lower(),
            parsed_url.netloc.lower(),
            parsed_url.path,
            parsed_url.params,
            parsed_url.query,
            parsed_url.fragment
        ))
        return sanitized_url
    except Exception:
        return None
