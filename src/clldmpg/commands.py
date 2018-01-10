# coding: utf8
from __future__ import unicode_literals, print_function, division
import os
import re

from clldutils.clilib import command
from clldutils.path import Path, read_text
from clldutils.jsonlib import load, update


def app_name(project_dir):
    setup = read_text(project_dir / 'setup.py')
    match = re.search('main\s*=\s*(?P<name>[a-z0-9]+):main', setup)
    if match:
        return match.group('name')


@command()
def dl2cdstar(args):
    app = app_name(args.project)
    if not app:
        args.log.error('cannot parse package name')
        return

    try:
        from cdstarcat.catalog import Catalog
    except ImportError:
        args.log.error('pip install cdstarcat')
        return

    title_pattern = re.compile('%s (?P<version>[0-9.]+) - downloads' % re.escape(app))
    title = '{0} {1} - downloads'.format(app, args.version)
    pkg_dir = args.project.joinpath(app)
    with Catalog(
            Path(os.environ['CDSTAR_CATALOG']),
            cdstar_url=os.environ['CDSTAR_URL'],
            cdstar_user=os.environ['CDSTAR_USER'],
            cdstar_pwd=os.environ['CDSTAR_PWD']) as cat:
        obj = cat.api.get_object()
        obj.metadata = {"creator": "pycdstar", "title": title}
        if args.args:
            obj.metadata["description"] = args.args[0]
        for fname in pkg_dir.joinpath('static', 'download').iterdir():
            if fname.is_file() and not fname.name.startswith('.'):
                print(fname.name)
                obj.add_bitstream(
                    fname=fname.as_posix(), name=fname.name.replace('-', '_'))
        cat.add(obj)

    fname = pkg_dir.joinpath('static', 'downloads.json')
    with update(fname, default={}, indent=4) as downloads:
        for oid, spec in load(Path(os.environ['CDSTAR_CATALOG'])).items():
            if 'metadata' in spec and 'title' in spec['metadata']:
                match = title_pattern.match(spec['metadata']['title'])
                if match:
                    if match.group('version') not in downloads:
                        spec['oid'] = oid
                        downloads[match.group('version')] = spec
    args.log.info('{0} written'.format(fname))
    args.log.info('{0}'.format(os.environ['CDSTAR_CATALOG']))
