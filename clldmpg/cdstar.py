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
from clld.web.util.helpers import icon
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
    return guess_type(obj.jsondata['original'])[0] or 'application/octet-stream'


def maintype(obj, mimetype_=None):
    mtype = mimetype_ or mimetype(obj)
    return mtype.split('/')[0]


def bitstream_url(obj, type_='original'):
    path = '/bitstreams/{0}/{1}'.format(
        obj.jsondata['objid'],
        obj.jsondata.get(type_) or obj.jsondata['original'])
    return SERVICE_URL.path(path).as_string()


ICON_FOR_MIMETYPE = {
    'facetime-video': [
        'video',
    ],
    'camera': [
        'image',
    ],
    'headphones': [
        'audio',
    ],
    'file': [
        'text',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ],
    'list': [
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/csv',
    ],
}
MIMETYPE_TO_ICON = {}
for icon_, types_ in ICON_FOR_MIMETYPE.items():
    for type_ in types_:
        MIMETYPE_TO_ICON[type_] = icon_


def link(obj, label=None, with_mime_type=True, badge=False):
    label = label or 'View file'
    mtype = mimetype(obj)
    icon_ = MIMETYPE_TO_ICON.get(
        mtype, MIMETYPE_TO_ICON.get(maintype(obj, mimetype_=mtype), 'download-alt'))
    md = ''
    if obj.jsondata.get('size'):
        md = format_size(obj.jsondata['size'])
    if with_mime_type:
        if md:
            md += ', '
        md += mtype
    if md:
        label += ' (%s)' % md
    return HTML.a(
        HTML.span(
            icon(icon_, inverted=badge),
            ' ' + label,
            class_='badge' if badge else 'cdstar_link'),
        href=bitstream_url(obj))


def linked_image(obj, check=True):
    if check and maintype(obj) != 'image':
        raise ValueError('type mismatch: {0} and image'.format(maintype(obj)))
    return HTML.a(
        HTML.img(src=bitstream_url(obj, 'web'), class_='image'),
        href=bitstream_url(obj),
        title="View image ({0})".format(format_size(obj.jsondata.get('size', 0))))


def _media(maintype_, obj, **kw):
    label = kw.pop('label', None)
    assert maintype_ in ['audio', 'video']
    if maintype(obj) != maintype_:
        raise ValueError('type mismatch: {0} and {1}'.format(maintype(obj), maintype_))
    kw.setdefault('controls', 'controls')
    media_element = getattr(HTML, maintype_)(
        literal('Your browser does not support the <code>{0}</code> element.'.format(
            maintype_)),
        HTML.source(src=bitstream_url(obj), type=mimetype(obj)), **kw)
    return HTML.div(
        media_element,
        HTML.br(),
        link(obj, label=label),
        class_='cdstar_{0}_link'.format(maintype_),
        style='margin-top: 10px')


audio = partial(_media, 'audio')


def video(obj, **kw):
    if obj.jsondata.get('thumbnail'):
        kw['poster'] = bitstream_url(obj, type_='thumbnail')
    return _media('video', obj, **kw)
