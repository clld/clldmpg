from pyramid.testing import Configurator


def test_MpgOlacConfig(mocker):
    from clldmpg import MpgOlacConfig

    cfg = MpgOlacConfig()
    assert cfg.admin(None).role == 'Admin'
    assert 'eva' in cfg.description(mocker.MagicMock())['institution'].url


def test_includeme():
    from clldmpg import includeme

    includeme(Configurator(settings={'sqlalchemy.url': 'sqlite://'}))
