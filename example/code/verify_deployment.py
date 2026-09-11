"""Exercise Compose port configuration in a separate, disposable test project."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import urllib.request

BOX = Path(__file__).resolve().parent.parent
PROJECT = 'idioca-docs-verification'
environment = dict(os.environ)
environment.pop('PORT', None)


def run(arguments, envfile, expected=True, override=None):
    env = dict(environment)
    if override is not None:
        env['PORT'] = override
    result = subprocess.run(
        ['docker', 'compose', '-p', PROJECT, '--env-file', str(envfile),
         '-f', str(BOX / 'compose.yml'), *arguments],
        env=env, capture_output=True, text=True, timeout=90)
    assert (result.returncode == 0) == expected, result.stdout + result.stderr
    return result.stdout


with tempfile.TemporaryDirectory() as folder:
    envfile = Path(folder) / '.env'
    envfile.write_text('PORT=8081\n')
    try:
        for override, expected in [(None, '8081'), ('8082', '8082'), ('', '8080')]:
            config = json.loads(run(['config', '--format', 'json'], envfile, override=override))
            port = config['services']['web']['ports'][0]
            assert str(port['published']) == expected
            assert port['host_ip'] == '127.0.0.1'
        envfile.write_text('')
        config = json.loads(run(['config', '--format', 'json'], envfile))
        assert str(config['services']['web']['ports'][0]['published']) == '8080'
        print('PASS: .env, shell precedence, empty/unset defaults, loopback binding', flush=True)

        envfile.write_text('PORT=8081\n')
        run(['up', '--build', '--wait', '--wait-timeout', '20'], envfile)
        with urllib.request.urlopen('http://127.0.0.1:8081/') as response:
            assert response.status == 200
        envfile.write_text('PORT=8082\n')
        run(['up', '--wait', '--wait-timeout', '20'], envfile)
        with urllib.request.urlopen('http://127.0.0.1:8082/') as response:
            assert response.status == 200
        try:
            urllib.request.urlopen('http://127.0.0.1:8081/', timeout=2)
        except OSError:
            pass
        else:
            raise AssertionError('Old port still responds')
        run(['down'], envfile)
        run(['up', '--build', '--wait', '--wait-timeout', '20'], envfile)
        with urllib.request.urlopen('http://127.0.0.1:8082/') as response:
            assert response.status == 200
        run(['down'], envfile)
        print('PASS: custom port, reconfiguration releases old port, removal/rebuild recovery', flush=True)

        # Default example must already be running on 8080 for occupied-port check.
        for invalid in ['80', '65536', 'abc', '8080']:
            envfile.write_text(f'PORT={invalid}\n')
            run(['up', '--wait', '--wait-timeout', '10'], envfile, expected=False)
            envfile.write_text('PORT=8082\n')
            run(['down'], envfile)
        print('PASS: below-range, above-range, non-integer and occupied ports fail', flush=True)
    finally:
        envfile.write_text('PORT=8082\n')
        run(['down'], envfile)
