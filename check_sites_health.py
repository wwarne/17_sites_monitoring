import requests
import whois

from urllib.parse import urlparse, urlunparse
from dateutil.parser import parse


def load_urls4check(path):
    yield from open(path, mode='r', encoding='utf-8')


def is_server_respond_with_200(url):
    try:
        resp = requests.get(url, allow_redirects=True)
    except requests.exceptions.RequestException:
        return False
    return resp.status_code == 200


def fetch_domain_expiration_date(domain_name):
    try:
        w = whois.whois(domain_name)
    except whois.parser.PywhoisError:
        return None
    expiration_date = w.expiration_date
    if isinstance(expiration_date, (tuple, list)):
        expiration_date = expiration_date[0]
    return expiration_date


def sanitize_address(url):
    url = url.rstrip('\n')
    parse_result = urlparse(url)
    scheme = parse_result or 'http'
    address = parse_result.netloc or parse_result.path
    return urlunparse((scheme, address, '', '', '', ''))

if __name__ == '__main__':
    pass
