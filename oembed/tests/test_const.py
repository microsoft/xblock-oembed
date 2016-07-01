""" Copyright (c) Microsoft Corporation. All Rights Reserved. """
""" Licensed under the MIT license. See LICENSE file on the project webpage for details. """

""" Constants used within tests """
# -*- coding: utf-8 -*-
#
# Constants ###########################################################
STUDIO_EDIT_WRAPPER = '<div class="wrapper-comp-settings is-active editor-with-buttons'
VALIDATION_WRAPPER = '<span class="xblock-editor-error-message">'
USER_INPUTS_WRAPPER = '<ul class="list-input settings-list">'
BUTTONS_WRAPPER = '<div class="xblock-actions">'

RESULT_SUCCESS = {'result': 'success'}
RESULT_ERROR = {'result': 'error'}
RESULT_MISSING_EVENT_TYPE = {'result': 'error', 'message': 'Missing display_name in JSON data'}

STATUS_CODE_200 = {'status_code': 200}
STATUS_CODE_400 = {'status_code': 400}
STATUS_CODE_404 = {'status_code': 404}
