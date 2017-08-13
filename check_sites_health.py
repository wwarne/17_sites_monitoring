from collections import namedtuple
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlunparse

import argparse
import requests
import whois
from dateutil.parser import parse

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
        whois_information = whois.whois(domain_name)
    except whois.parser.PywhoisError:
        return
    if isinstance(whois_information.expiration_date, (tuple, list)):
        return whois_information.expiration_date[0]
    return whois_information.expiration_date


def is_server_respond_with_200(url):
    try:
        resp = requests.get(url, allow_redirects=True)
    except requests.exceptions.RequestException:
        return False
    return resp.ok


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


def bool2human(value_to_convert):
    if value_to_convert is None:
        return 'N/A'
    elif value_to_convert:
        return 'YES'
    else:
        return 'NO'


def date2string(date_to_convert):
    if date_to_convert is None:
        return 'N/A'
    if not isinstance(date_to_convert, datetime):
        return str(date_to_convert)
    return date_to_convert.strftime('%d.%m.%Y %H:%M:%S')


def pretty_format(domain_obj):
    if not isinstance(domain_obj, Domain):
        return
    return '{:<30}|{:^10}|{:^10}|{:^15}'.format(domain_obj.url,
                                                bool2human(domain_obj.is_respond_200),
                                                bool2human(domain_obj.is_expire),
                                                date2string(domain_obj.expire_date))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sites Monitoring Utility')
    parser.add_argument('path', help='Path to a file with a list of websites to check.')
    parameters = parser.parse_args()

    websites = load_urls4check(parameters.path)
    print('Today is: {}'.format(date2string(datetime.now())))
    print('{:<30}|{:^10}|{:^10}|{:^15}'.format('Domain', 'Working', 'Expiring', 'Expire date'))
    for website in websites:
        print('{:-<75}'.format(''))
        site_info = collect_domain_info(website)
        print(pretty_format(site_info))
