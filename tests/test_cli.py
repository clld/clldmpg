import pathlib
import collections

import pytest

from clldmpg.__main__ import main, ProjectDirType, app_name


@pytest.fixture
def project_dir(tmpdir):
    tmpdir.join('setup.py').write_text("'paste.app_factory': ['main=app:main']", encoding='utf8')
    tmpdir.join('app', 'static', 'download').ensure(dir=True)
    tmpdir.join('app', 'static', 'download', 'test.txt').write_text('test', encoding='utf8')
    return str(tmpdir)


def test_help(capsys, project_dir):
    with pytest.raises(SystemExit):
        main([])

    with pytest.raises(SystemExit):
        main(['--project', str(pathlib.Path(__file__).parent)])

    main(['--project', project_dir])
    out, _ = capsys.readouterr()
    assert 'usage' in out


def test_ProjectDirType(project_dir):
    d = ProjectDirType()(project_dir)
    assert app_name(d) == 'app'


def test_main(mocker, project_dir):
    mocker.patch('clldmpg.commands.dl2cdstar.run', lambda args: True)
    main(['--project', project_dir, 'dl2cdstar'])


def test_dl2cdstar(project_dir, mocker, tmpdir):
    tmpdir.join('cat.json').write_text(
        '{"OID": {"metadata": {"title": "app 2.1 - downloads"}}}', encoding='utf8')
    os_ = mocker.Mock(
        environ=collections.defaultdict(lambda: '', CDSTAR_CATALOG=str(tmpdir.join('cat.json'))))
    mocker.patch('clldmpg.commands.dl2cdstar.os', os_)
    mocker.patch('clldmpg.commands.dl2cdstar.Catalog', mocker.MagicMock())
    main(['--project', project_dir, 'dl2cdstar', '--version', '2.1', '--description', 'xy'])
    tmpdir.join('app', 'static', 'downloads.json').ensure()
