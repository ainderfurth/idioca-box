"""Produce the three offline pages from the only declared content inputs."""
from html import escape
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '.tools'))
import markdown

DOCUMENTS = (
    ('IdiocaSpec.md', 'index.html', 'Idioca Box Spec'),
    ('LICENSE', 'license.html', 'Creative Commons Attribution 4.0 International'),
    ('README.md', 'readme.html', 'Idioca Box'),
)


def build(root=HERE.parent.parent, output=HERE):
    # Read and render every input before writing anything: missing inputs must fail.
    sources = [(name, page, label, (root / name).read_text(encoding='utf-8-sig'))
               for name, page, label in DOCUMENTS]
    pages = {}
    for name, page, label, source in sources:
        assert label in source, f'Navigation label is no longer present in {name}'
        navigation = '\n'.join(
            f'<a href="{target}"' + (' aria-current="page"' if target == page else '')
            + f'>{escape(title)}</a>' for _, target, title in DOCUMENTS)
        body = (f'<pre class="license">{escape(source)}</pre>' if name == 'LICENSE'
                else markdown.markdown(source, extensions=['fenced_code', 'tables', 'sane_lists']))
        pages[page] = f'''<!doctype html>
<html lang="en" data-webtui-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(label)}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<nav box-="square">{navigation}</nav>
<main box-="double"><article>{body}</article></main>
</body>
</html>
'''
    output.mkdir(parents=True, exist_ok=True)
    for page, content in pages.items():
        (output / page).write_text(content, encoding='utf-8', newline='\n')


if __name__ == '__main__':
    try:
        build()
    except (OSError, UnicodeError, AssertionError) as error:
        sys.exit(f'Website generation failed: {error}')
    print('Generated index.html, license.html and readme.html.')
