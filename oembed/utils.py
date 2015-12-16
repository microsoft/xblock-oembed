from const import OEMBED_SERVICES
import re
import urllib2
import json
from filter import Filter


def get_embed_html(url):

    # check if it already is an embed code
    embed_code_regex = '<iframe '
    matched = re.match(embed_code_regex, url, re.IGNORECASE)

    if matched is not None:
        return url

    # match the url against url patterns for various services to determine the source of the document and then convert
    # the url into an embed code depending upon whether the service supports OEmbed protocol
    for service, urls in OEMBED_SERVICES.iteritems():
        matched = re.match(urls['regex'], url, re.IGNORECASE)

        if matched is not None:
            res = json.load(urllib2.urlopen(urls['embed_url'].format(url)))
            return res['html']

    return Filter.EMBED_CODE_TEMPLATE.format(url)
