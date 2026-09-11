"""Static example server; only packaged HTML and CSS assets are public."""
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent


class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        path = unquote(urlsplit(self.path).path)
        if path == '/':
            self.path = '/index.html'
            path = '/index.html'
        target = (ROOT / path.lstrip('/')).resolve()
        if (not target.is_relative_to(ROOT) or not target.is_file()
                or target.suffix not in {'.html', '.css'}):
            self.send_error(404)
            return None
        return super().send_head()


if __name__ == '__main__':
    port = os.environ.get('PORT') or '8080'
    if not re.fullmatch(r'[0-9]+', port) or len(port) > 5 or not 1024 <= int(port) <= 65535:
        sys.exit('PORT must be an integer from 1024 to 65535.')
    # PORT is the host publication setting; the private container listener is fixed.
    server = ThreadingHTTPServer(('0.0.0.0', 8080), partial(Handler, directory=str(ROOT)))
    print(f'Serving documentation; configured host port {port}', flush=True)
    server.serve_forever()
