import requests
import whois
from urllib.parse import urlparse, urlunparse
from dateutil.parser import parse
from datetime import datetime, timedelta
from collections import namedtuple


Domain = namedtuple('Domain', ['url', 'is_respond_200', 'is_expire', 'expire_date'])


def load_urls4check(path):
    yield from open(path, mode='r', encoding='utf-8')


def sanitize_address(url):
    url = url.rstrip('\n')
    parse_result = urlparse(url)
    scheme = parse_result.scheme or 'http'
    address = parse_result.netloc or parse_result.path
    return urlunparse((scheme, address, '', '', '', ''))


def get_domain_expiration_date(domain_name):
    try:
        w = whois.whois(domain_name)
    except whois.parser.PywhoisError:
        return
    if isinstance(w.expiration_date, (tuple, list)):
        return w.expiration_date[0]
    return w.expiration_date


def is_server_respond_with_200(url):
    try:
        resp = requests.get(url, allow_redirects=True)
    except requests.exceptions.RequestException:
        return False
    return resp.status_code == 200


def is_expire_in_month(expire_date):
    if not expire_date:
        return
    if isinstance(expire_date, str):
        try:
            expire_date = parse(expire_date)
        except ValueError:
            return
    month_from_now = datetime.now() + timedelta(days=30)
    return expire_date <= month_from_now


def collect_domain_info(url):
    url = sanitize_address(url)
    expire_date = get_domain_expiration_date(url)
    return Domain(url=url,
                  is_respond_200=is_server_respond_with_200(url),
                  is_expire=is_expire_in_month(expire_date),
                  expire_date=expire_date)


def bool2human(value):
    if value is None:
        return 'N/A'
    elif value:
        return 'YES'
    else:
        return 'NO'


def date2string(value):
    if value is None:
        return 'N/A'
    if not isinstance(value, datetime):
        return str(value)
    return value.strftime('%d.%m.%Y %H:%M:%S')


def pretty_format(domain_obj):
    if not isinstance(domain_obj, Domain):
        return
    url = domain_obj.url
    respond = bool2human(domain_obj.is_respond_200)
    expire = bool2human(domain_obj.is_expire)
    expire_date = date2string(domain_obj.expire_date)
    return '{:<30}{:<15}{:<15}{:<15}'.format(url, respond, expire, expire_date)


if __name__ == '__main__':
    websites = load_urls4check('test.txt')
    print('{:<30}{:<15}{:<15}{:<15}'.format('Domain', 'Working', 'Expiring', 'Expire date'))
    for website in websites:
        site_info = collect_domain_info(website)
        print(pretty_format(site_info))
