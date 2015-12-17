import unittest
import json
from workbench.runtime import WorkbenchRuntime
from xblock.runtime import KvsFieldData, DictKeyValueStore
from oembed.tests.test_utils import generate_scope_ids, make_request
from oembed import OEmbedXBlock
from mock import Mock
from nose.tools import assert_equals, assert_in
from oembed.tests.test_const import STUDIO_EDIT_WRAPPER, VALIDATION_WRAPPER, USER_INPUTS_WRAPPER, STATUS_CODE_200
from oembed.tests.test_const import BUTTONS_WRAPPER, RESULT_SUCCESS, RESULT_ERROR, STATUS_CODE_404, STATUS_CODE_400
from oembed.filter import EMBED_CODE_TEMPLATE
from oembed.oembed import DEFAULT_DOCUMENT_URL


# Constants ###########################################################
TEST_SUBMIT_DATA = {
    'display_name': "OEmbed",
    'document_url': DEFAULT_DOCUMENT_URL
}

TEST_INCOMPLETE_DATA = {
    'document_url': DEFAULT_DOCUMENT_URL
}


class TestOEmbedBlock(unittest.TestCase):
    """ Tests for OEmbedBlock """

    @classmethod
    def make_oembed_block(cls):
        """ helper to construct a OEmbedBlock """
        runtime = WorkbenchRuntime()
        key_store = DictKeyValueStore()
        db_model = KvsFieldData(key_store)
        ids = generate_scope_ids(runtime, 'oembed')
        return OEmbedXBlock(runtime, db_model, scope_ids=ids)

    def test_oembed_template_content(self):  # pylint: disable=no-self-use
        """ Test content of OEmbedXblock's rendered views """
        block = TestOEmbedBlock.make_oembed_block()
        block.usage_id = Mock()

        student_fragment = block.render('student_view', Mock())
        assert_in('<div class="oembed-xblock" id="oembed_block_container"', student_fragment.content)
        assert_in('OEmbed', student_fragment.content)
        assert_in(EMBED_CODE_TEMPLATE.format(DEFAULT_DOCUMENT_URL), student_fragment.content)

        studio_fragment = block.render('studio_view', Mock())
        assert_in(STUDIO_EDIT_WRAPPER, studio_fragment.content)
        assert_in(VALIDATION_WRAPPER, studio_fragment.content)
        assert_in(USER_INPUTS_WRAPPER, studio_fragment.content)
        assert_in(BUTTONS_WRAPPER, studio_fragment.content)

    def test_studio_document_submit(self):
        """ Test studio submission of OEmbedBlock """
        block = TestOEmbedBlock.make_oembed_block()

        body = json.dumps(TEST_SUBMIT_DATA)
        res = block.handle('studio_submit', make_request(body))
        # pylint: disable=no-value-for-parameter
        assert_equals(json.loads(res.body), RESULT_SUCCESS)

        assert_equals(block.display_name, TEST_SUBMIT_DATA['display_name'])
        assert_equals(block.document_url, TEST_SUBMIT_DATA['document_url'])

        body = json.dumps('')
        res = block.handle('studio_submit', make_request(body))
        assert_equals(json.loads(res.body), RESULT_ERROR)


