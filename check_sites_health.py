import requests

from urllib.parse import urlparse, urlunparse


def load_urls4check(path):
    yield from open(path, mode='r', encoding='utf-8')


def is_server_respond_with_200(url):
    try:
        resp = requests.get(url, allow_redirects=True)
    except requests.exceptions.RequestException:
        return False
    return resp.status_code == 200


def get_domain_expiration_date(domain_name):
    pass


def sanitize_address(url):
    url = url.rstrip('\n')
    parse_result = urlparse(url)
    scheme = parse_result or 'http'
    address = parse_result.netloc or parse_result.path
    return urlunparse((scheme, address, '', '', '', ''))

if __name__ == '__main__':
    pass
