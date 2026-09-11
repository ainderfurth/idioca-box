# Idioca Box Contract: Idioca documentation website

**Contract version:** 0.2.0  
**Status:** Draft — example implementation available  
**Maintainers:** Idioca Box repository maintainers

## 1. Purpose and scope

Provide a minimal, understandable example of an Idioca box: a website that presents the repository's specification, license and README and demonstrates that the same contracted capability can be used directly from the filesystem or through a locally deployed container.

The workload is to present a static website with three linked pages, one for each of the repository's three source files. The specification is the entry page; the license and README each have their own page. The example must be simple enough for a human to understand its purpose, run it and verify its behaviour using the README alone.

Authentication, user accounts, data entry, persistent user data, application APIs and production hosting are outside its scope.

## 2. Interfaces

| Interface | Input or action | Required output or effect |
|---|---|---|
| Local file | Open `code/index.html` in a browser | Display the complete, styled website without starting a server or running a build command |
| Container deployment | Start the box using the root `compose.yml` | Make the website available at `http://localhost:<PORT>/` on the host, using port 8080 by default |
| Configuration | Set `PORT` in the box-root `.env`, using `.env.example` as a starting point | Publish the website on the configured host port; website content and local-file mode remain unchanged |
| HTTP page | `GET /` or `GET /index.html` | HTTP 200 with an HTML document presenting the same website as local-file mode |
| Other document pages | `GET /license.html` or `GET /readme.html` | HTTP 200 with the license or repository-root README respectively; all three pages link to one another |
| HTTP assets | Request a stylesheet or other asset referenced by the page | HTTP 200 with the appropriate content type and asset contents |
| Missing HTTP resource | Request an unknown path, such as `/missing` | HTTP 404; do not silently substitute the documentation page |

The container's published port must be bound to host loopback only. No application API is exposed beyond retrieving the website and its assets.

If container startup fails, for example because Docker is unavailable or the configured port is invalid or occupied, the startup command must report a failure. It must not silently select another port. A running container alone is not evidence that the website is ready; a successful HTTP request is.

## 3. Semantic contract

The entire contents of repository-root `IdiocaSpec.md`, `LICENSE` and `README.md` are the website's sole text-content inputs; their contents are presented on three linked pages. Relative to this box, these are `../IdiocaSpec.md`, `../LICENSE` and `../README.md`. The example's own contract, README and configuration files are not website content inputs. This contract governs behaviour and presentation; it does not supply website copy.

Markdown may be rendered as HTML while preserving its wording, document structure, code examples and link labels and destinations. The license must retain its complete text. Formatting and layout may change, but content must not be summarized, rewritten or omitted. No greeting, explanation, navigation label, caption or other website copy may be invented; textual UI labels and the document title must use text already present in the three source files. Linked documents and websites must not be imported as additional content.

The website must represent the source files as they exist when it is produced. Updating a source file requires refreshing the website through a documented process; live synchronization is not required. Missing or unreadable inputs must cause that process to fail explicitly rather than produce a partial website. The delivered local HTML must already contain the content and must not require runtime fetching of the source files.

The page must:

* Present each source document on its own linked page, preserving the reading order within each document.
* Use WebTUI CSS to provide a terminal-style presentation. WebTUI is an explicit requirement of this example; the server, base image and internal build tools are implementation choices.
* Present the same content and styling in both access modes. Both modes must present the same source-document content.
* Be readable at viewport widths of 375px and 1280px without horizontal page scrolling.

All resources needed to display the page must be supplied with the box. Local-file mode must work without an internet connection. The page must not depend on JavaScript execution, request remote fonts or CDN assets, set cookies, use browser storage or send analytics.

## 4. Dependencies and configuration

A modern browser supporting local HTML files and the CSS features used by WebTUI is required for viewing. The implementation's README must identify the browsers used for verification.

Container mode additionally requires a running Docker engine supporting Linux containers and Docker Compose v2. Building or obtaining the container may require internet access; viewing the website after deployment must not require external services.

The host port is configurable to demonstrate external configuration. `PORT` is a non-secret setting; no secrets are required by this box.

| Setting | Meaning | Allowed values | Default |
|---|---|---|---|
| `PORT` | Host TCP port used to access the containerized website | Integer from 1024 to 65535; the port must be available | 8080 when unset or empty |

The box-root `.env.example` must include `PORT=8080` and explain its meaning and allowed values. Users may copy it to `.env` and change the value. `.env` must remain outside version control and may be omitted to use the default address, `http://localhost:8080/`. An externally supplied shell value for `PORT` takes precedence over `.env`; if the resulting value is unset or empty, the default applies. Port changes take effect when the deployment is reapplied, not merely when `.env` is edited.

Changing `PORT` changes only the host HTTP address. The loopback-only binding, website content and local-file mode remain unchanged. Any configuration introduced later that changes observable behaviour must first be declared in this contract, including its default and meaning.

The implementation must document the WebTUI version supplied and preserve its applicable license notices. Replacing the HTTP server or container base image must not require consumers to change how they use the website.

## 5. State and storage

The three repository-root source documents are authoritative inputs and must not be modified by the box. The website is a reproducible representation of those inputs. The box creates and owns no authoritative runtime state. It must not modify the supplied website files while serving them. Temporary server files, logs and caches must be disposable.

No persistent volume or `data/` directory is required. Stopping, removing, rebuilding or replacing the container must lose no user information. Recovery consists of obtaining the implementation files again and reopening the page or redeploying the container.

## 6. Verification

| Acceptance criterion | Required evidence |
|---|---|
| Content comes solely from the declared inputs | Compare the website with all three source files; verify complete content, preserved wording and no added website copy |
| Source changes are reproducible | Change a source document in a test copy and follow the documented refresh process; verify that the website reflects the change |
| Invalid inputs fail explicitly | Make a source file unavailable in a test copy; verify that producing the website fails rather than succeeds with missing content |
| Local use needs no server or build | Open the delivered `code/index.html` directly; verify all three documents and styling |
| Local use works offline | Disable networking and reopen the file; all content and styling still appear |
| Container deployment works | Follow the README from a fresh checkout with Docker running; request `http://localhost:8080/` and receive HTTP 200 with the specification; follow the links to the license and README and receive their complete contents with HTTP 200 |
| Port configuration works | Set `PORT=8081` in `.env` with no shell override, reapply the deployment and verify the website at `http://localhost:8081/`; verify that this deployment no longer publishes port 8080 |
| Configuration precedence and defaults hold | Verify that a shell value overrides `.env`, and that an unset or empty effective value uses port 8080 |
| Invalid or occupied ports fail visibly | Try an out-of-range value, a non-integer value and an occupied port; startup must fail without silently choosing another port |
| Access modes are equivalent | Compare local-file and HTTP views; content and styling match |
| Presentation remains readable | Inspect both modes at 375px and 1280px widths; no horizontal page scrolling |
| HTTP assets and errors are correct | Request the page's assets and an unknown path; verify success with appropriate content types and HTTP 404 respectively |
| Browser behaviour stays within scope | Inspect network activity and browser storage; no external requests, cookies or application storage |
| Deployment stays local | Inspect the published port binding; it is limited to host loopback |
| Replacement is disposable | Remove and rebuild the container, then request the page successfully without restoring runtime data |

These are acceptance requirements, not claims of completed testing. A replacement implementation must satisfy the same criteria. The choice of verification tools remains open.

## 7. Deployment and operation

The box must follow the root structure defined in the [Idioca Box Spec](../IdiocaSpec.md). `code/index.html` is the local entry point and `compose.yml` is the container deployment entry point. The root is a project and deployment folder; it does not prescribe the container's internal filesystem layout.

The README must provide a short, precise guide for both usage modes, including prerequisites, the exact commands to start and stop the container, the working directory for each command and the URL to open. It must show how to configure `PORT` through `.env`, reapply the deployment and use the resulting URL. It must also show an HTTP request example and its expected result, explain how to inspect service status and logs, and describe recovery from startup failures.

The example's README must also explain how to refresh the delivered website after the repository-root source documents change. These operational instructions are not additional website content.

Once started, the container serves requests until stopped. HTTP access and server errors must be observable through the documented logging interface. Stopping the container must release its published port. No backup or migration procedure is needed for runtime data.

## 8. System composition and orchestration

The user opens the local file or starts the container and visits the HTTP address. Each page request triggers the complete workload. The box has no peer-service dependencies and requires no orchestration beyond its single-service deployment.

Consumers rely on the declared file and HTTP interfaces. They do not depend on the HTTP server implementation or the container's internal paths.

## Change history

| Contract version | Date | Change | Migration |
|---|---|---|---|
| 0.1.0 | 2026-09-11 | Initial draft for the hello-world website example | Not applicable; no implementation yet |
| 0.2.0 | 2026-09-11 | Replace greeting content with the complete repository-root specification, license and README as the sole text inputs | Contract only; no implementation yet |
