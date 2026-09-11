"""Boundary checks; optional HTTP and browser checks use the delivered artifacts."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import shutil
import tempfile
import urllib.error
import urllib.request

from build import DOCUMENTS, HERE, build


class Content(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_article = False
        self.text = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'article':
            self.in_article = True
        if tag == 'a' and self.in_article:
            self.links.append(dict(attrs)['href'])

    def handle_endtag(self, tag):
        if tag == 'article':
            self.in_article = False

    def handle_data(self, data):
        if self.in_article:
            self.text.append(data)


def check_sources():
    root = HERE.parent.parent
    with tempfile.TemporaryDirectory() as folder:
        temp = Path(folder)
        source = temp / 'source'
        source.mkdir()
        for name, _, _ in DOCUMENTS:
            shutil.copyfile(root / name, source / name)
        output = temp / 'output'
        build(source, output)
        for _, page, _ in DOCUMENTS:
            assert (output / page).read_bytes() == (HERE / page).read_bytes(), f'Stale page: {page}'
        license_page = Content()
        license_page.feed((output / 'license.html').read_text(encoding='utf-8'))
        assert ''.join(license_page.text) == (source / 'LICENSE').read_text(encoding='utf-8-sig')
        marker = 'Unique verification input: <unsafe> & unchanged text.'
        with (source / 'README.md').open('a', encoding='utf-8') as file:
            file.write('\n\n' + marker.replace('<unsafe>', '`<unsafe>`') + '\n')
        build(source, output)
        parsed = Content()
        parsed.feed((output / 'readme.html').read_text(encoding='utf-8'))
        assert marker in ''.join(parsed.text)
        before = {p.name: p.read_bytes() for p in output.iterdir()}
        (source / 'LICENSE').unlink()
        try:
            build(source, output)
        except FileNotFoundError:
            pass
        else:
            raise AssertionError('Missing source was accepted')
        assert before == {p.name: p.read_bytes() for p in output.iterdir()}
    print('PASS: source snapshot, complete license, changed input, missing-input failure without partial output')


def check_http(url):
    for path in ['index.html', 'license.html', 'readme.html', 'style.css',
                 'vendor/base.css', 'vendor/utils/box.css', 'vendor/components/typography.css']:
        with urllib.request.urlopen(url + '/' + path) as response:
            assert response.status == 200
            assert response.headers.get_content_type() == ('text/css' if path.endswith('.css') else 'text/html')
            assert response.read() == (HERE / path).read_bytes()
    with urllib.request.urlopen(url + '/') as response:
        assert response.read() == (HERE / 'index.html').read_bytes()
    for path in ['/missing', '/server.py', '/vendor/', '/../contract.md']:
        try:
            urllib.request.urlopen(url + path)
        except urllib.error.HTTPError as error:
            assert error.code == 404
        else:
            raise AssertionError(f'Unexpected public resource: {path}')
    print('PASS: HTTP content, CSS types, file/HTTP byte equivalence, missing/private resource 404s')


def check_browser(url):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel='msedge', headless=True)
        print('Browser:', browser.version)
        for mode in ['file', 'http'] if url else ['file']:
            context = browser.new_context(java_script_enabled=False, offline=(mode == 'file'))
            for width in [375, 1280]:
                page = context.new_page()
                page.set_viewport_size({'width': width, 'height': 900})
                requests, errors = [], []
                page.on('request', lambda request: requests.append(request.url))
                page.on('requestfailed', lambda request: errors.append(request.url))
                for _, name, _ in DOCUMENTS:
                    address = (HERE / name).as_uri() if mode == 'file' else url + '/' + name
                    page.goto(address, wait_until='networkidle')
                    assert not errors, errors
                    assert all(r.startswith('file:') if mode == 'file' else r.startswith(url + '/') for r in requests)
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                    assert page.locator('article').inner_text().strip()
                    assert page.locator('nav a').count() == 3
                    assert page.evaluate("getComputedStyle(document.body).backgroundColor") == 'rgb(17, 25, 23)'
                    assert page.evaluate("getComputedStyle(document.querySelector('main'), '::before').content") != 'none'
                    assert page.evaluate("document.querySelectorAll('script').length") == 0
                    if mode == 'http':
                        assert page.evaluate('localStorage.length + sessionStorage.length') == 0
                page.goto((HERE / 'index.html').as_uri() if mode == 'file' else url + '/', wait_until='networkidle')
                page.locator('nav a[href="license.html"]').click()
                assert page.url.endswith('license.html')
                page.close()
            assert context.cookies() == []
            context.close()
        browser.close()
    print('PASS: offline/HTTP browser views, no external requests or scripts/storage, navigation, 375px/1280px layout, WebTUI borders')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url')
    parser.add_argument('--browser', action='store_true')
    args = parser.parse_args()
    check_sources()
    if args.url:
        check_http(args.url.rstrip('/'))
    if args.browser:
        check_browser(args.url.rstrip('/') if args.url else None)
