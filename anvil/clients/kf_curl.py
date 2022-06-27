#!/usr/bin/env python3

"""Send query to multiple FHIR endpoints, consume all pages, write results to stdout."""

import json
import logging
import os
import urllib.parse as urlparse

import click
from click_loglevel import LogLevel
from fhirclient.server import FHIRJSONMimeType

from anvil.clients.fhir_client import DispatchingFHIRClient
from anvil.clients.smart_auth import KidsFirstFHIRAuth

LOG_FORMAT = '%(asctime)s %(name)s %(levelname)-8s %(message)s'


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(threadName)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)


def worker(server, path=None, no_sign=False, headers={}):
    """Callback handler"""

    def fetch(url, _headers):
        """Low level GET, follow next links.
         see https://github.com/smart-on-fhir/client-py/blob/master/fhirclient/server.py#L174."""
        header_defaults = {
            'Accept': FHIRJSONMimeType,
            'Accept-Charset': 'UTF-8',
        }
        # merge in user headers with defaults
        header_defaults.update(_headers)
        _headers = header_defaults
        if not no_sign and server.auth is not None and server.auth.can_sign_headers():
            _headers = server.auth.signed_headers(_headers)
        # perform the request but intercept 401 responses, raising our own Exception
        res = server.session.get(url, headers=_headers)
        server.raise_for_status(res)
        __json = res.json()
        __next = None
        if 'link' in __json:
            _links = {lnk['relation']: lnk['url'] for lnk in __json['link']}
            if 'next' in _links:
                __next = _links['next']
        return __json, __next

    # main
    assert path, "caller MUST pass path"
    if path.startswith('/'):
        path = path[1:]
    initial_url = urlparse.urljoin(server.base_uri, path)
    _url = initial_url
    while _url:
        (_json, _url) = fetch(_url, _headers=headers)
        print(json.dumps(_json, separators=(',', ':')), flush=True)


def _dispatch(url, token):
    """Manufacture URLs, dispatch to thread."""

    api_bases = [url]

    settings = {
        'app_id': __name__,
        'api_bases': api_bases
    }
    client = DispatchingFHIRClient(settings=settings, auth=KidsFirstFHIRAuth(cookie=token))
    client.prepare()
    assert client.ready, "server should be ready"
    client.dispatch(worker, path=url)


def _get_token_help():
    token = kids_first_cookie()
    if token:
        return f"{token[0:10]}..."
    return """see https://github.com/NIH-NCPI/FHIR-CAT-June22/blob/main/Kids_First.md#supplying-the-cookie-for-programmatic-requests"""


def kids_first_cookie():
    """AWSELBAuthSessionCookie cookie captured from https://kf-api-fhir-service.kidsfirstdrc.org browser"""
    assert 'KIDS_FIRST_COOKIE' in os.environ
    assert os.environ['KIDS_FIRST_COOKIE'].startswith('AWSELBAuthSessionCookie')
    return os.environ['KIDS_FIRST_COOKIE']


@click.command()
@click.option('--token', default=kids_first_cookie(), help=f'env var. KIDS_FIRST_COOKIE [default: {_get_token_help()}]')
@click.option("-l", "--log-level", type=LogLevel(), default=logging.INFO)
@click.argument('url', required=True)
def cli(token, url, log_level):
    """Query FHIR service and retrieve entire bundle.

        url: FHIR compliant url 'eg https://kf-api-fhir-service.kidsfirstdrc.org/ResearchStudy
    """
    logging.basicConfig(level=log_level, format=LOG_FORMAT, force=True)
    logger.setLevel(log_level)
    assert logging.getLogger(__name__).level != logging.NOTSET, f"Should be {log_level}"
    _dispatch(url, token)


if __name__ == '__main__':
    cli()
