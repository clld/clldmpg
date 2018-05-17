# coding: utf8
from __future__ import unicode_literals, print_function, division


def test_links(testapp):
    body = testapp.get('/legal').body.decode('utf8')
    assert 'https://www.shh.mpg.de/138116/privacy-policy' in body
    assert 'Privacy Policy' in body
    assert 'https://www.shh.mpg.de/2435/imprint' in body
