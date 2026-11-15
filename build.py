#!/usr/bin/env python3
"""Wrap content/*.html in layout.html and write the site pages."""

import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "html"

PAGES = [
    ("index.html", "Welcome to Openvario | Openvario"),
    ("flight-computer.html", "The Flight Computer - Overview | Openvario"),
    ("mechanics.html", "The Flight Computer - Mechanics | Openvario"),
    ("hardware.html", "The Flight Computer - Hardware | Openvario"),
    ("software.html", "The Flight Computer - Software | Openvario"),
    ("protocol.html", "The Flight Computer - OV Protocol | Openvario"),
    ("projects.html", "Projects | Openvario"),
    ("download.html", "Download | Openvario"),
    ("license.html", "License | Openvario"),
    ("variants.html", "Variants | Openvario"),
]

TOP = [
    ("index.html", "Home"),
    ("flight-computer.html", "The Flight Computer"),
    ("projects.html", "Projects"),
    ("download.html", "Download"),
    ("license.html", "License"),
]

FLIGHT = [
    ("flight-computer.html", "Overview"),
    ("mechanics.html", "Mechanics"),
    ("hardware.html", "Hardware"),
    ("software.html", "Software"),
    ("protocol.html", "OpenVario Protocol"),
]


def link(href, label, current):
    current_attr = ' aria-current="page"' if href == current else ""
    return f'<a href="{href}"{current_attr}>{escape(label)}</a>'


def nav(current):
    top = "".join(f"<li>{link(href, label, current)}</li>" for href, label in TOP)
    sub = "".join(f"<li>{link(href, label, current)}</li>" for href, label in FLIGHT)
    return f'<ul class="top">{top}</ul><ul class="sub">{sub}</ul>'


def main():
    layout = (ROOT / "layout.html").read_text()
    OUT.mkdir(exist_ok=True)
    missing = []
    for name, title in PAGES:
        body = (ROOT / "content" / name).read_text().strip()
        for ref in re.findall(r'(?:src|href)="(images/[^"]+)"', body):
            if not (ROOT / ref).is_file():
                missing.append(f"{name}: {ref}")
        page = (
            layout.replace("{{title}}", escape(title))
            .replace("{{nav}}", nav(name))
            .replace("{{content}}", body)
        )
        if "{{" in page:
            sys.exit(f"unfilled slot in {name}")
        page = page.replace('href="style.css"', 'href="../style.css"')
        page = page.replace('src="images/', 'src="../images/')
        page = page.replace('href="images/', 'href="../images/')
        text = page if page.endswith("\n") else page + "\n"
        (OUT / name).write_text(text)
        (ROOT / name).unlink(missing_ok=True)
    for ref in re.findall(r'(?:src|href)="(images/[^"]+)"', layout):
        if not (ROOT / ref).is_file():
            missing.append(f"layout: {ref}")
    content_files = sorted(p.name for p in (ROOT / "content").glob("*.html"))
    page_files = sorted(name for name, _ in PAGES)
    if content_files != page_files:
        sys.exit(f"content files {content_files} != pages {page_files}")
    if missing:
        sys.exit("missing images:\n" + "\n".join(missing))


if __name__ == "__main__":
    main()
