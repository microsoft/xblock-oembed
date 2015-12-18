""" 
The "Oembed XBlock" allows course staffers to embed files/vidoes stored in various internet file storage services to the courseware (courseware, course info and syllabus)
by adding a link through an advanced component that they create in edX's Studio authoring tool. The files or videos can be added as embedded content.
""" 

import textwrap

import pkg_resources
import requests

from xblock.core import XBlock
from xblock.fragment import Fragment
from xblock.fields import Scope, String
from filter import EMBED_CODE_TEMPLATE

import logging

LOG = logging.getLogger(__name__)
from filter import Filter

DEFAULT_DOCUMENT_URL = ('https://onedrive.live.com/embed?cid=ADC6477D8F22FD9D&resid=ADC6477D8F22FD9D%21104&authkey=AFWEOfGpKb8L29w&em=2&wdStartOn=1')

class OEmbedXBlock(XBlock):

    display_name = String(
        display_name="Display Name",
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="OEmbed",
    )

    document_url = String(
        display_name="Document URL",
        help="Navigate to the document in your browser and ensure that it is public. Copy its URL and paste it into this field.",
        scope=Scope.settings,
        default=DEFAULT_DOCUMENT_URL
    )

    reference_name = String(
        display_name="Reference Name",
        help="The link text.",
        scope=Scope.settings,
        default=""
    )

    output_model = String(
        display_name="Ouput Model",
        help="Currently selected option for how to insert the document into the unit.",
        scope=Scope.settings,
        default="1"
    )
    
    model1 = String(
        display_name="Model1 preselection",
        help="Previous selection.",
        scope=Scope.settings,
        default=""
    )	

    model2 = String(
        display_name="Model2 preselection",
        help="Previous selection.",
        scope=Scope.settings,
        default=""
    )	

    # model3 = String(
        # display_name="Model3 preselection",
        # help="Previous selection.",
        # scope=Scope.settings,
        # default="selected=selected"
    # )	

    output_code = String(
        display_name="Output Iframe Embed Code",
        help="Copy the embed code into this field.",
        scope=Scope.settings,
        default=EMBED_CODE_TEMPLATE.format(DEFAULT_DOCUMENT_URL)
    )

    message = String(
        display_name="Document display status message",
        help="Message to help students in case of errors.",
        scope=Scope.settings,
        default="Note: Some services may require you to be signed into them to access documents stored there."
    )

    message_display_state = String(
        display_name="Whether to display the status message",
        help="Determines whether to display the message to help students in case of errors.",
        scope=Scope.settings,
        default="block"
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the OEmbedXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/oembed.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/oembed.css"))
        frag.add_javascript(self.resource_string("static/js/src/oembed.js"))
        frag.initialize_js('OEmbedXBlock')
        return frag

    def studio_view(self, context=None):
        """
        he primary view of the OEmbedXBlock, shown to teachers
        when viewing courses.
        """

        html = self.resource_string("static/html/oembed_edit.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/oembed.css"))
        frag.add_javascript(self.resource_string("static/js/src/oembed_edit.js"))
        frag.initialize_js('OEmbedXBlock')
        return frag

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):  # pylint: disable=unused-argument
        """
        Change the settings for this XBlock given by the Studio user
        """
        if not isinstance(submissions, dict):
            LOG.error("submissions object from Studio is not a dict - %r", submissions)
            return {
                'result': 'error'
            }

        self.document_url = submissions['document_url']

        self.output_code = Filter.get_embed_code(url=self.document_url)
        self.message = "Note: Some services may require you to be signed into them to access documents stored there."
        self.message_display_state = "block"

        return {'result': 'success'}

    @XBlock.json_handler
    def check_url(self, data, suffix=''):  # pylint: disable=unused-argument,no-self-use
        """
        Checks that the given document url is accessible, and therefore assumed to be valid
        """
        try:
            test_url = data['url']
        except KeyError as ex:
            LOG.debug("URL not provided - %s", unicode(ex))
            return {
                'status_code': 400,
            }

        try:
            url_response = requests.head(test_url)
        # Catch wide range of request exceptions
        except requests.exceptions.RequestException as ex:
            LOG.debug("Unable to connect to %s - %s", test_url, unicode(ex))
            return {
                'status_code': 400,
            }

        return {
            'status_code': url_response.status_code,
        }

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("OEmbedXBlock",
             """<vertical_demo>
                <oembed/>
                <oembed/>
                <oembed/>
                </vertical_demo>
             """),
        ]
