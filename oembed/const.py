""" Copyright (c) Microsoft Corporation. All Rights Reserved. """
""" Licensed under the MIT license. See LICENSE file on the project webpage for details. """

OEMBED_SERVICES = {

    'youtube': {
        'regex': '(https?:\/\/(www\.)?)(youtube\.com|youtu\.be|youtube\.googleapis.com)\/(?:embed\/|v\/|watch\?v=|watch\?.+&amp;v=|watch\?.+&v=)?((\w|-){11})(.*?)',
        'embed_url': 'http://www.youtube.com/oembed?url={}&format=json'
    },

    'ted': {
        'regex': '(https?:\/\/(www\.)?)(ted\.com)\/talks',
        'embed_url': 'http://www.ted.com/services/v1/oembed.json?url={}'
    },

    'vimeo': {
        'regex': 'https?:\/\/(www\.)?vimeo\.com\/',
        'embed_url': 'https://vimeo.com/api/oembed.json?url={}'
    },

    'office_mix': {
        'regex': '(https?:\/\/(www\.)?)(mix\.office\.com)/watch',
        'embed_url': 'https://mix.office.com/oembed/?url={}'
    },

    'slideshare': {
        'regex': 'https?:\/\/(www\.)?slideshare\.net',
        'embed_url': 'http://www.slideshare.net/api/oembed/2?url={}&format=json'
    },

    'issuu': {
        'regex': 'https?:\/\/(www\.)?issuu\.com',
        'embed_url': 'http://issuu.com/oembed?url={}&format=json'
    },

    'soundcloud': {
        'regex': 'https?:\/\/(www\.)?soundcloud\.com',
        'embed_url': 'http://soundcloud.com/oembed?url={}&format=json'
    },

}
