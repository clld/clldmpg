# coding: utf8
from __future__ import unicode_literals, print_function, division
from unittest import TestCase

from mock import Mock


class Tests(TestCase):
    def test_bitstream_url(self):
        from clldmpg.cdstar import bitstream_url

        obj = Mock(jsondata=dict(objid='x', original='y'))
        self.assertTrue(bitstream_url(obj).endswith('/x/y'))

        obj = Mock(jsondata=dict(objid='x', other='y'))
        self.assertTrue(bitstream_url(obj, type_='other').endswith('/x/y'))

    def test_media(self):
        from clldmpg.cdstar import audio, video, linked_image

        obj = Mock(jsondata=dict(objid='x', original='1'))
        self.assertRaises(ValueError, video, obj)

        obj = Mock(jsondata=dict(objid='x', original='a.mp4'))
        self.assertIn('<video', video(obj))
        self.assertRaises(ValueError, audio, obj)
        self.assertRaises(ValueError, linked_image, obj)

        obj = Mock(jsondata=dict(objid='x', original='a.jpeg'))
        self.assertIn('<img', linked_image(obj))
