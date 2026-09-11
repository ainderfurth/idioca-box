# Idioca documentation website

Read the repository specification, license and README as three linked WebTUI pages. The [contract](contract.md) defines the behaviour.

## Open from disk

Open [code/index.html](code/index.html) in a modern browser (double-click it in your file manager). Follow the navigation links to the license and README. Keep the supplied files in `code/` together. No server, build command, internet connection or JavaScript is needed.

## Start on localhost

Start Docker Desktop with Linux containers, or another Linux Docker engine with Compose v2. From the repository root:

```sh
cd example
docker compose up --build --wait
```

Open **http://localhost:8080/**. The same three pages appear. The command waits for a successful HTTP health check and exits unsuccessfully if startup fails. The initial build may download the Python base image. All subsequent commands below run from `example/`.

## Configure the port

Copy `.env.example` to `.env` using your file manager, or run one of:

```powershell
# PowerShell
Copy-Item .env.example .env
```

```sh
# POSIX shell
cp .env.example .env
```

Set `PORT=8081` in `.env`, then run:

```sh
docker compose up --build --wait
```

Open **http://localhost:8081/**. Choose an available integer port from 1024 to 65535. An exported shell `PORT` overrides `.env`; an unset or empty effective value uses 8080. No `.env` is required for defaults, and `.env` is ignored by Git. Editing `.env` alone does not change a running container. File mode and page content are unaffected.

Compose publishes only on `127.0.0.1`. Use `http://127.0.0.1:8080/` if your machine resolves localhost only to IPv6.

## Verify, diagnose and stop

```sh
docker compose ps
docker compose logs web
curl -i http://localhost:8080/
curl -i http://localhost:8080/license.html
curl -i http://localhost:8080/readme.html
curl -i http://localhost:8080/style.css
curl -i http://localhost:8080/missing
```

On Windows PowerShell use `curl.exe`. Substitute your configured port. Expect HTTP 200 and the specification, license and README respectively, HTTP 200 with CSS, then HTTP 404. There is no application API. Logs expose requests and server errors; `ps` shows health and the published port.

If Docker is unavailable, start the engine. For an invalid or occupied port, correct `PORT` or choose a free port and reapply the deployment. The box never automatically selects another port.

```sh
docker compose down
```

This removes the container and releases the port. Recreate it with `docker compose up --build --wait`. No runtime data needs backup or migration.

## Refresh the website

The committed HTML is a snapshot of **only** the repository-root `IdiocaSpec.md`, `LICENSE` and `README.md`. After editing those source files, use Python 3.10 or newer:

```sh
python -m pip install --target .tools -r code/requirements.txt
python code/build.py
```

Generation reads all three inputs before writing the pages and fails if an input is missing or unreadable. Review and commit the regenerated HTML with source changes. Reopen the file; for container mode, rebuild with `docker compose up --build --wait`. Serving never reads or changes the source files. Original Markdown link destinations are preserved, so links to repository files outside the three-page website may be unavailable in the deployed site.

The box uses WebTUI 0.1.10, supplied locally under its [MIT license](code/vendor/LICENSE), and Python-Markdown 3.8.2 for generation. The container uses `python:3.13-alpine`; the minor-version tag can receive upstream updates. The server and generator are implementation details. No `data/` directory is needed.

## Acceptance checks

```sh
python code/verify.py
```

This checks document fidelity, deterministic generation, source changes and missing-input failure without editing the authoritative inputs. For HTTP checks with the container running:

```sh
python code/verify.py --url http://localhost:8080
```

Browser verification instructions and the results for this implementation are recorded in [VERIFICATION.md](VERIFICATION.md).
