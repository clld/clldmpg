# coding: utf8
"""
For all clld apps hosted by MPI SHH, we store all binary content (e.g. multi-media files)
in our CDSTAR [1] instance hosted at GWDG. This module provides functionality to integrate
these binary objects in clld apps.

[1] https://info.gwdg.de/docs/doku.php?id=en:services:storage_services:gwdg_cdstar:start
"""
from __future__ import unicode_literals, print_function, division
from mimetypes import guess_type
from functools import partial

from purl import URL
from clld.web.util.htmllib import HTML, literal
from clldutils.misc import format_size

SERVICE_URL = URL("https://cdstar.shh.mpg.de/")


def mimetype(obj):
    if hasattr(obj, 'mimetype'):
        return obj.mimetype
    if hasattr(obj, 'mime_type'):
        return obj.mime_type
    if obj.jsondata.get('mimetype'):
        return obj.jsondata['mimetype']
    if obj.jsondata.get('mime_type'):
        return obj.jsondata['mime_type']
    return guess_type(obj.jsondata['original'])[0]


def maintype(obj):
    mtype = mimetype(obj)
    if mtype is None:
        return
    return mtype.split('/')[0]


def bitstream_url(obj, type_='original'):
    path = '/bitstreams/{0}/{1}'.format(
        obj.jsondata['objid'],
        obj.jsondata.get(type_) or obj.jsondata['original'])
    return SERVICE_URL.path(path).as_string()


def linked_image(obj, check=True):
    if check and maintype(obj) != 'image':
        raise ValueError('type mismatch: {0} and image'.format(maintype(obj)))
    return HTML.a(
        HTML.img(src=bitstream_url(obj, 'web'), class_='image'),
        href=bitstream_url(obj),
        title="view image [{0}]".format(format_size(obj.jsondata.get('size', 0))))


def _media(maintype_, obj, **kw):
    assert maintype_ in ['audio', 'video']
    if maintype(obj) != maintype_:
        raise ValueError('type mismatch: {0} and {1}'.format(maintype(obj), maintype_))
    kw.setdefault('controls', 'controls')
    return getattr(HTML, maintype_)(
        literal('Your browser does not support the <code>{0}</code> element.'.format(
            maintype_)),
        'You can download the file from',
        HTML.a('here', href=bitstream_url(obj)),
        HTML.source(src=bitstream_url(obj), type=mimetype(obj)), **kw)


audio = partial(_media, 'audio')


def video(obj, **kw):
    if obj.jsondata.get('thumbnail'):
        kw['poster'] = bitstream_url(obj, type_='thumbnail')
    return _media('video', obj, **kw)
