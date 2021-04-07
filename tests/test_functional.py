
def test_links(testapp):
    body = testapp.get('/legal').body.decode('utf8')
    assert 'eva.mpg.de/privacy-policy' in body
    assert 'Privacy Policy' in body
    assert 'imprint.html' in body
