# OpenVario website

Static site. Page text is in `content/`. The shared header and nav are `layout.html`. Looks are `style.css`. Pictures are in `images/`.

```bash
python3 build.py
ln -s ../../hooks/pre-commit .git/hooks/pre-commit
```

Built pages are written to `html/`. Serve this directory as the site root and open `html/`. The pre-commit hook runs only when HTML is staged, rebuilds the pages, and stops the commit if `html/` was left unstaged.
