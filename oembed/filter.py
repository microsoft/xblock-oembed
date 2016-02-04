import textwrap
import logging
LOG = logging.getLogger(__name__)
from const import OEMBED_SERVICES
import re
import urllib2
import json

EMBED_CODE_TEMPLATE = textwrap.dedent("""
        <iframe
            src="{}"
            frameborder="0"
            width="960"
            height="569"
            allowfullscreen="true"
            mozallowfullscreen="true"
            webkitallowfullscreen="true">
        </iframe>
    """)
# Helper class to map the document URL into a form required for adding to the courseware, depending upon how it is intended to be used
class Filter:

    @staticmethod
    def get_embed_code(url):
        url = url.strip()
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

        return EMBED_CODE_TEMPLATE.format(url)
