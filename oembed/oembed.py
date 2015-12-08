""" 
The "File Storage XBlock" allows course staffers to add files stored in various internet file storage services to the courseware (courseware, course info and syllabus) 
by adding a link through an advanced component that they create in edX's Studio authoring tool. The files can be added either as embedded content, 
or as links to the files in their original location.
""" 

import textwrap

import pkg_resources
import urllib2
import mimetypes

from xblock.core import XBlock
from xblock.fragment import Fragment
from xblock.fields import Scope, String
from django.conf import settings

import logging
from functools import partial
from cache_toolbox.core import del_cached_content

from xmodule.contentstore.django import contentstore
from xmodule.contentstore.content import StaticContent
from opaque_keys.edx.keys import CourseKey
LOG = logging.getLogger(__name__)
from filter import Filter

DEFAULT_DOCUMENT_URL = ('https://onedrive.live.com/embed?cid=ADC6477D8F22FD9D&resid=ADC6477D8F22FD9D%21104&authkey=AFWEOfGpKb8L29w&em=2&wdStartOn=1')

class OembedXBlock(XBlock):

    display_name = String(
        display_name="Display Name",
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="Oembed",
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
        default=Filter.EMBED_CODE_TEMPLATE.format(DEFAULT_DOCUMENT_URL)
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
        The primary view of the OembedXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/oembed.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/oembed.css"))
        frag.add_javascript(self.resource_string("static/js/src/oembed.js"))
        frag.initialize_js('OembedXBlock')
        return frag

    def studio_view(self, context=None):
        """
        he primary view of the OembedXBlock, shown to teachers
        when viewing courses.
        """

        html = self.resource_string("static/html/oembed_edit.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/oembed.css"))
        frag.add_javascript(self.resource_string("static/js/src/oembed_edit.js"))
        frag.initialize_js('OembedXBlock')
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

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("OembedXBlock",
             """<vertical_demo>
                <oembed/>
                <oembed/>
                <oembed/>
                </vertical_demo>
             """),
        ]
