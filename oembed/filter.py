import textwrap
from utils import get_embed_html
import logging
LOG = logging.getLogger(__name__)


# Helper class to map the document URL into a form required for adding to the courseware, depending upon how it is intended to be used
class Filter():
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

    @staticmethod
    def get_embed_code(url):
        url = url.strip()
        return get_embed_html(url)
