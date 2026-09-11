# Verification

Verified on 2026-09-11 against contract 0.2.0, including the clarified three-page layout.

## Results

- Source snapshot checks passed: regenerated pages match the delivered HTML, the license text is complete, changed source text appears after regeneration, and a missing source fails without partial output.
- Docker image built and the service became healthy at http://localhost:8080/.
- HTTP checks passed for all three pages and four CSS assets, including content types and byte equality with local files. Unknown paths and private implementation resources returned 404.
- Microsoft Edge 152.0.4191.66 passed browser checks at 375px and 1280px widths in both file and HTTP modes. File mode ran with networking disabled and JavaScript disabled. Navigation worked, WebTUI borders loaded, and no horizontal page scrolling, external requests, scripts, cookies or browser storage were found.
- A separate Compose test project verified `.env` configuration, shell precedence, unset/empty defaults and loopback publication. Switching from port 8081 to 8082 released 8081; removing and rebuilding restored service without data recovery.
- Below-range, above-range, non-integer and occupied host ports all caused startup failure. The test project's containers and network were removed afterward.

Firefox and Safari have not been tested. The original source documents include repository-relative links beyond these three pages; their destinations are preserved as required, but those resources are not part of the deployed website.

## Repeat the checks

From `example/`, install the generation dependency and run:

```sh
python -m pip install --target .tools -r code/requirements.txt
python code/verify.py
docker compose up --build --wait
python code/verify.py --url http://localhost:8080
```

For browser checks, install the optional verification dependency and have Microsoft Edge installed:

```sh
python -m pip install --target .tools playwright==1.55.0
python code/verify.py --url http://localhost:8080 --browser
```

For deployment checks, leave the default example running on port 8080 and ensure ports 8081 and 8082 are free:

```sh
python code/verify_deployment.py
```

This command creates and removes the separate `idioca-docs-verification` Compose project. It does not edit your `.env` or change the default example deployment.
