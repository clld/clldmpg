from pyramid.response import Response


def includeme(config):
    config.add_static_view('clldmpg-static', 'clldmpg:static')
    config.add_settings({'clld.publisher_logo': 'clldmpg:static/minerva.png'})

    config.add_route('google-site-verification', 'googlebbc8f4da1abdc58b.html')
    config.add_view(
        lambda r: Response('google-site-verification: googlebbc8f4da1abdc58b.html'),
        route_name='google-site-verification')
