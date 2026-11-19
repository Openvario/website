# OpenVario website

https://test.openvario.de/

Static site. Page text is in `content/`. The shared header and nav are `layout.html`. Looks are `style.css`. Pictures are in `images/`.

```bash
python3 build.py
pre-commit install
```

Built pages are written to `html/`. Serve this directory as the site root and open `html/`. Pre-commit runs Prettier on source files and rebuilds the pages; it stops the commit if `html/` was left unstaged. Pull requests run the same checks via `.github/workflows/pre-commit.yml`.
