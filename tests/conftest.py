# coding: utf8
from __future__ import unicode_literals, print_function, division

import pytest
from pyramid import config
from clld.db.meta import DBSession, Base
from clld.db.models import common
from pytest_clld._app import ExtendedTestApp


@pytest.fixture(scope='module')
def testapp():
    def main():
        cfg = config.Configurator(settings={
            'sqlalchemy.url': 'sqlite://',
            'mako.directories': ['clldmpg:templates', 'clld:web/templates']})
        cfg.include('clldmpg')
        return cfg.make_wsgi_app()

    DBSession.remove()
    wsgi_app = main()
    Base.metadata.bind = DBSession.bind
    Base.metadata.create_all()
    DBSession.add(common.Dataset(id='1', name='test app', domain='example.org'))
    yield ExtendedTestApp(wsgi_app)
