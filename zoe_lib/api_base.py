"""
This package contains the Zoe library, with modules used by more than one of the Zoe components. This library can also be used to write new clients for Zoe.
"""
from functools import wraps
import logging
import time

import requests
import requests.exceptions

from zoe_lib.version import ZOE_API_VERSION
from zoe_lib.exceptions import ZoeAPIException

log = logging.getLogger(__name__)


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    log.warning(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


class ZoeAPIBase:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

    @retry(ZoeAPIException)
    def _rest_get(self, path):
        """
        :type path: str
        :rtype: (dict, int)
        """
        url = self.url + '/api/' + ZOE_API_VERSION + path
        try:
            r = requests.get(url, auth=(self.user, self.password))
        except requests.exceptions.Timeout:
            raise ZoeAPIException('HTTP connection timeout')
        except requests.exceptions.HTTPError:
            raise ZoeAPIException('Invalid HTTP response')
        except requests.exceptions.ConnectionError as e:
            raise ZoeAPIException('Connection error: {}'.format(e))

        try:
            data = r.json()
        except ValueError:
            data = None
        return data, r.status_code

    @retry(ZoeAPIException)
    def _rest_post(self, path, payload):
        """
        :type path: str
        :rtype: (dict, int)
        """
        url = self.url + '/api/' + ZOE_API_VERSION + path
        try:
            r = requests.post(url, auth=(self.user, self.password), json=payload)
        except requests.exceptions.Timeout:
            raise ZoeAPIException('HTTP connection timeout')
        except requests.exceptions.HTTPError:
            raise ZoeAPIException('Invalid HTTP response')
        except requests.exceptions.ConnectionError as e:
            raise ZoeAPIException('Connection error: {}'.format(e))

        try:
            data = r.json()
        except ValueError:
            data = None
        return data, r.status_code

    @retry(ZoeAPIException)
    def _rest_delete(self, path):
        """
        :type path: str
        :rtype: (dict, int)
        """
        url = self.url + '/api/' + ZOE_API_VERSION + path
        try:
            r = requests.delete(url, auth=(self.user, self.password))
        except requests.exceptions.Timeout:
            raise ZoeAPIException('HTTP connection timeout')
        except requests.exceptions.HTTPError:
            raise ZoeAPIException('Invalid HTTP response')
        except requests.exceptions.ConnectionError as e:
            raise ZoeAPIException('Connection error: {}'.format(e))

        try:
            data = r.json()
        except ValueError:
            data = None
        return data, r.status_code
