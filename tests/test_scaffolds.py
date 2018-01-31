from __future__ import unicode_literals


def test_ClldAppTemplate(tmpdir, mocker):
    from clldmpg.scaffolds import ClldAppTemplate

    tmpl = ClldAppTemplate('clld_app')
    tmpl.run(
        mocker.Mock(
            verbosity=0,
            options=mocker.Mock(simulate=False, interactive=False, overwrite=False)),
        str(tmpdir),
        {
            'project': 'test-project',
            'package': 'pkg',
            'package_logger': 'pkg',
        },
    )
    tmpdir.ensure('pkg', 'views.py')
    tmpdir.ensure('migrations', 'env.py')
