from pyramid.response import Response

from clld.interfaces import IOlacConfig
from clld.web.views.olac import OlacConfig, Participant, Institution


class MpgOlacConfig(OlacConfig):
    def description(self, req):
        return {
            'archiveURL': 'http://%s/' % req.dataset.domain,
            'participants': [
                Participant("Admin", 'Robert Forkel', 'forkel@shh.mpg.de'),
            ] + [
                Participant(
                    "Editor",
                    ed.contributor.name,
                    ed.contributor.email or req.dataset.contact)
                for ed in req.dataset.editors],
            'institution': Institution(
                'Max Planck Institute for the Science of Human History',
                'http://shh.mpg.de',
                'Jena, Germany',
            ),
            'synopsis': req.dataset.description or '',
        }


def includeme(config):
    config.registry.registerUtility(MpgOlacConfig(), IOlacConfig)
    config.include('clld.web.app')
    config.add_static_view('clldmpg-static', 'clldmpg:static')
    config.add_settings({'clld.publisher_logo': 'clldmpg:static/minerva.png'})

    config.add_route('google-site-verification', 'googlebbc8f4da1abdc58b.html')
    config.add_view(
        lambda r: Response('google-site-verification: googlebbc8f4da1abdc58b.html'),
        route_name='google-site-verification')
