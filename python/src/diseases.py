from __future__ import print_function
import sys
import json

HEADER = {'User-Agent': 'RealTimeWeb Diseases library for educational purposes'}
PYTHON_3 = sys.version_info >= (3, 0)

if PYTHON_3:
    import urllib.error
    import urllib.request as request
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus

# Embed your own keys for simplicity
CONSUMER_KEY = "your key goes here"
CONSUMER_SECRET = "your key goes here"
ACCESS_TOKEN = "your key goes here"
ACCESS_TOKEN_SECRET = "your key goes here"
# Remove these lines; we just do this for our own simplicity
with open('../src/secrets.txt', 'r') as secrets:
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = \
        [l.strip() for l in secrets.readlines()]


# Auxilary


def _parse_float(value, default=0.0):
    """
    Attempt to cast *value* into a float, returning *default* if it fails.
    """
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _iteritems(_dict):
    """
    Internal method to factor-out Py2-to-3 differences in dictionary item
    iterator methods

    :param dict _dict: the dictionary to parse
    :returns: the iterable dictionary
    """
    if PYTHON_3:
        return _dict.items()
    else:
        return _dict.iteritems()


def _urlencode(query, params):
    """
    Internal method to combine the url and params into a single url string.

    :param str query: the base url to query
    :param dict params: the parameters to send to the url
    :returns: a *str* of the full url
    """
    return query + '?' + '&'.join(key + '=' + quote_plus(str(value))
                                  for key, value in _iteritems(params))


def _get(url):
    """
    Internal method to convert a URL into it's response (a *str*).

    :param str url: the url to request a response from
    :returns: the *str* response
    """
    if PYTHON_3:
        req = request.Request(url, headers=HEADER)
        response = request.urlopen(req)
        return response.read().decode('utf-8')
    else:
        req = urllib2.Request(url, headers=HEADER)
        response = urllib2.urlopen(req)
        return response.read()


def _recursively_convert_unicode_to_str(input):
    """
    Force the given input to only use `str` instead of `bytes` or `unicode`.

    This works even if the input is a dict, list, or a string.

    :params input: The bytes/unicode input
    :returns str: The input converted to a `str`
    """
    if isinstance(input, dict):
        return {_recursively_convert_unicode_to_str(
            key): _recursively_convert_unicode_to_str(value) for key, value in
                input.items()}
    elif isinstance(input, list):
        return [_recursively_convert_unicode_to_str(element) for element in
                input]
    elif not PYTHON_3:
        return input.encode('utf-8')
    elif PYTHON_3 and isinstance(input, str):
        return str(input.encode('ascii', 'replace').decode('ascii'))
    else:
        return input


# Cache

_CACHE = {}
_CACHE_COUNTER = {}
_EDITABLE = False
_CONNECTED = True
_PATTERN = "repeat"


def _start_editing(pattern="repeat"):
    """
    Start adding seen entries to the cache. So, every time that you make a request,
    it will be saved to the cache. You must :ref:`_save_cache` to save the
    newly edited cache to disk, though!
    """
    global _EDITABLE, _PATTERN
    _EDITABLE = True
    _PATTERN = pattern


def _stop_editing():
    """
    Stop adding seen entries to the cache.
    """
    global _EDITABLE
    _EDITABLE = False


def _add_to_cache(key, value):
    """
    Internal method to add a new key-value to the local cache.
    :param str key: The new url to add to the cache
    :param str value: The HTTP response for this key.
    :returns: void
    """
    if key in _CACHE:
        _CACHE[key].append(value)
    else:
        _CACHE[key] = [_PATTERN, value]
        _CACHE_COUNTER[key] = 0


def _clear_key(key):
    """
    Internal method to remove a key from the local cache.
    :param str key: The url to remove from the cache
    """
    if key in _CACHE:
        del _CACHE[key]


def _save_cache(filename="cache.json"):
    """
    Internal method to save the cache in memory to a file, so that it can be used later.

    :param str filename: the location to store this at.
    """
    with open(filename, 'w') as f:
        json.dump({"data": _CACHE, "metadata": ""}, f)


def _lookup(key):
    """
    Internal method that looks up a key in the local cache.

    :param key: Get the value based on the key from the cache.
    :type key: string
    :returns: void
    """
    if key not in _CACHE:
        return ""
    if _CACHE_COUNTER[key] >= len(_CACHE[key][1:]):
        if _CACHE[key][0] == "empty":
            return ""
        elif _CACHE[key][0] == "repeat" and _CACHE[key][1:]:
            return _CACHE[key][-1]
        elif _CACHE[key][0] == "repeat":
            return ""
        else:
            _CACHE_COUNTER[key] = 1
    else:
        _CACHE_COUNTER[key] += 1
    if _CACHE[key]:
        return _CACHE[key][_CACHE_COUNTER[key]]
    else:
        return ""


def connect():
    """
    Connect to the online data source in order to get up-to-date information.

    :returns: void
    """
    global _CONNECTED
    _CONNECTED = True


def disconnect(filename="../src/cache.json"):
    """
    Connect to the local cache, so no internet connection is required.

    :returns: void
    """
    global _CONNECTED, _CACHE
    try:
        with open(filename, 'r') as f:
            _CACHE = _recursively_convert_unicode_to_str(json.load(f))['data']
    except (OSError, IOError) as e:
        raise DiseasesException(
            "The cache file '{}' was not found.".format(filename))
    for key in _CACHE.keys():
        _CACHE_COUNTER[key] = 0
    _CONNECTED = False


# Exceptions

class DiseasesException(Exception):
    pass


# Domain Objects


class Diseases(object):
    """
    A Diseases contains
    """

    def __init__(self):

        """
        Creates a new diseases

        :returns: Diseases
        """
        raise NotImplementedError("Function Not Finished")

    def __unicode__(self):
        raise NotImplementedError("Function Not Finished")
        string = """ <Diseases Field: Value> """
        return string.format()

    def __repr__(self):
        string = self.__unicode__()

        if not PYTHON_3:
            return string.encode('utf-8')

        return string

    def __str__(self):
        string = self.__unicode__()

        if not PYTHON_3:
            return string.encode('utf-8')

        return string

    def _to_dict(self):
        raise NotImplementedError("Function Not Finished")

    @staticmethod
    def _from_json(json_data):
        """
        Creates a Diseases from json data.

        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Diseases
        """
        raise NotImplementedError("Function Not Finished")
        if json_data is None:
            return Diseases()
        try:
            diseases = Diseases(NEED_PARAMS)
            return diseases
        except KeyError:
            raise DiseasesException("The given information was incomplete.")


# Service Methods


def _fetch_diseases_info(params):
    """
    Internal method to form and query the server

    :param dict params: the parameters to pass to the server
    :returns: the JSON response object
    """
    from collections import OrderedDict

    baseurl = 'http://think.cs.vt.edu:5000/diseasess'
    # An ordered dictionary is necessary since an ordinary dictionary has no ordering which causes
    # problems when trying to retrieve an item from the cache
    ordered_dict = OrderedDict(
        sorted(_iteritems(params), key=lambda x: x[1], reverse=True))
    query = _urlencode(baseurl, ordered_dict)

    if PYTHON_3:
        try:
            result = _get(query) if _CONNECTED else _lookup(query)
        except urllib.error.HTTPError:
            raise DiseasesException("Make sure you entered a valid query")
    else:
        try:
            result = _get(query) if _CONNECTED else _lookup(query)
        except urllib2.HTTPError:
            raise DiseasesException("Make sure you entered a valid query")

    if not result:
        raise DiseasesException("There were no results")

    result = result.replace("// ", "")  # Remove Double Slashes
    result = " ".join(
        result.split())  # Remove Misc 1+ Spaces, Tabs, and New Lines

    try:
        if _CONNECTED and _EDITABLE:
            _add_to_cache(query, result)
        json_res = json.loads(result)
    except ValueError:
        raise DiseasesException("Internal Error")

    return json_res


def get_diseases_information(query):
    """
    Forms and poses the query to get information from the database
    :param query: the values to retrieve
    :return: the JSON response
    """
    if not isinstance(query, str):
        raise DiseasesException("Please enter a valid query")

    params = {'where': query}
    json_res = _fetch_diseases_info(params)
    json_list = json_res['_items']

    diseasess = []

    for json_dict in json_list:
        diseases = Diseases._from_json(json_res)
        diseasess.append(diseases._to_dict())

    return diseasess






