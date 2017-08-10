import requests

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

if __name__ == '__main__':
    pass
