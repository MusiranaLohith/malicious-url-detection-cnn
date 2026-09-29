import re
from urllib.parse import urlparse

def extract_features_59(url):
    features = []

    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path
    query = parsed.query

    # --- BASIC ---
    features.append(len(url))
    features.append(url.count('@'))
    features.append(url.count('?'))
    features.append(url.count('-'))
    features.append(url.count('='))
    features.append(url.count('.'))
    features.append(url.count('#'))
    features.append(url.count('%'))
    features.append(url.count('+'))
    features.append(url.count('$'))
    features.append(url.count('!'))
    features.append(url.count('*'))
    features.append(url.count(','))
    features.append(url.count('//'))

    # --- DIGITS / LETTERS ---
    features.append(sum(c.isdigit() for c in url))
    features.append(sum(c.isalpha() for c in url))

    # --- DOMAIN ---
    features.append(len(domain))
    features.append(domain.count('.'))

    # --- SECURITY ---
    features.append(1 if url.startswith("https") else 0)

    ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'
    features.append(1 if re.search(ip_pattern, url) else 0)

    # --- QUERY ---
    features.append(len(query))
    features.append(query.count('&'))

    # --- PATH ---
    features.append(len(path))
    features.append(path.count('/'))
    features.append(path.count('='))

    # --- PHISH WORDS ---
    words = ['login', 'verify', 'update', 'secure', 'bank']
    features.append(1 if any(w in url.lower() for w in words) else 0)

    # --- FILL TO 59 ---
    while len(features) < 59:
        features.append(0)

    return features