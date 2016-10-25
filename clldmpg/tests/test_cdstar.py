# coding: utf8
from __future__ import unicode_literals, print_function, division
from unittest import TestCase


class MockObject(object):
    def __init__(self, jsondata, **attrs):
        self.jsondata = jsondata
        for k, v in attrs.items():
            setattr(self, k, v)


class Tests(TestCase):
    def test_mimetype(self):
        from clldmpg.cdstar import mimetype

        self.assertEqual(mimetype(MockObject({}, mimetype='x')), 'x')
        self.assertEqual(mimetype(MockObject({}, mime_type='x')), 'x')
        self.assertEqual(mimetype(MockObject({'mimetype': 'x'})), 'x')
        self.assertEqual(mimetype(MockObject({'mime_type': 'x'})), 'x')

    def test_bitstream_url(self):
        from clldmpg.cdstar import bitstream_url

        obj = MockObject(dict(objid='x', original='y'))
        self.assertTrue(bitstream_url(obj).endswith('/x/y'))

        obj = MockObject(dict(objid='x', other='y'))
        self.assertTrue(bitstream_url(obj, type_='other').endswith('/x/y'))

    def test_media(self):
        from clldmpg.cdstar import audio, video, linked_image

        obj = MockObject(dict(objid='x', original='1'))
        self.assertRaises(ValueError, video, obj)

        obj = MockObject(dict(objid='x', original='a.mp4', thumbnail='a.jpg'))
        self.assertIn('<video', video(obj))
        self.assertIn('poster=', video(obj))
        self.assertRaises(ValueError, audio, obj)
        self.assertRaises(ValueError, linked_image, obj)

        obj = MockObject(dict(objid='x', original='a.jpeg'))
        self.assertIn('<img', linked_image(obj))
