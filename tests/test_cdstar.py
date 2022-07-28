import pytest
from clldmpg.cdstar import *


class MockObject(object):
    def __init__(self, jsondata, **attrs):
        self.jsondata = jsondata
        for k, v in attrs.items():
            setattr(self, k, v)


@pytest.mark.parametrize(
    "jsondata,kw,expected",
    [
        ({}, dict(mimetype='x'), 'x'),
        ({}, dict(mime_type='x'), 'x'),
        ({'mimetype': 'x'}, dict(), 'x'),
        ({'mime_type': 'x'}, dict(), 'x'),
        ({'mediaType': 'x'}, dict(), 'x'),
    ])
def test_mimetype(jsondata, kw, expected):
    assert mimetype(MockObject(jsondata, **kw)) == expected


@pytest.mark.parametrize(
    "jsondata,kw,endswith",
    [
        (dict(objid='x', original='y'), {}, '/x/y'),
        (dict(objid='x', other='y'), dict(type_='other'), '/x/y'),
        (dict(downloadUrl='http://example.org'), {}, 'example.org'),
    ]
)
def test_bitstream_url(jsondata, kw, endswith):
    obj = MockObject(jsondata)
    assert bitstream_url(obj, **kw).endswith(endswith)


def test_MediaCol(mocker):
    col = MediaCol(mocker.MagicMock(), 'name', 'audio')
    assert '<i' in \
        col.format(mocker.MagicMock(_files=[MockObject({}, mime_type='audio/x-wav')]))
    col = MediaCol(mocker.MagicMock(), 'name', 'other')
    assert col.format(mocker.MagicMock(_files=[MockObject({}, mime_type='other/x-wav')]))\
        == ''


def test_media():
    obj = MockObject(dict(objid='x', original='1'))
    with pytest.raises(ValueError):
        video(obj)

    obj = MockObject(dict(objid='x', original='a.mp4', thumbnail='a.jpg', size=10345))
    assert '<video' in video(obj)
    assert 'poster=' in video(obj)
    with pytest.raises(ValueError):
        audio(obj)
    with pytest.raises(ValueError):
        linked_image(obj)

    obj = MockObject(dict(objid='x', original='a.jpeg'))
    assert '<img' in linked_image(obj)
