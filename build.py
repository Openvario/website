#!/usr/bin/env python3
"""Wrap content/*.html in layout.html and write the site pages."""

import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "html"
SITE = "https://openvario.de/html/"

PAGES = [
    ("index.html", "Welcome to Openvario | Openvario", "Openvario is a project that aims to create a high performance, open source flight computer."),
    ("flight-computer.html", "The Flight Computer - Overview | Openvario", "A panel-mounted glide computer with a sunlight-readable display, for individuals and gliding clubs to build."),
    ("mechanics.html", "The Flight Computer - Mechanics | Openvario", "Housing, 3D model, and pressure-tube connectors for the Openvario flight computer."),
    ("hardware.html", "The Flight Computer - Hardware | Openvario", "The Openvario flight computer boards: Cubieboard, display, adapter, sensors, and RJ45."),
    ("software.html", "The Flight Computer - Software | Openvario", "Openvario software: OpenEmbedded Linux, sensor and vario daemons, the boot menu, and XCSoar."),
    ("protocol.html", "The Flight Computer - OV Protocol | Openvario", "The OpenVario NMEA protocol used between the sensor daemon, vario daemon, and XCSoar."),
    ("projects.html", "Projects | Openvario", "Projects page. It had no body text on openvario.de."),
    ("download.html", "Download | Openvario", "Software images for Openvario, hosted on the project's GitHub page."),
    ("license.html", "License | Openvario", "Openvario licenses: GPLv3 for software and CC BY-SA for documentation and hardware files."),
    ("variants.html", "Variants | Openvario", "Display variants of the Openvario flight computer that have been built."),
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


def link(href, label, current, section=False):
    if href == current:
        attr = ' aria-current="page"'
    elif section:
        attr = ' class="here"'
    else:
        attr = ""
    return f'<a href="{href}"{attr}>{escape(label)}</a>'


def nav(current):
    flight_hrefs = {href for href, _ in FLIGHT}
    in_flight = current in flight_hrefs
    items = []
    for href, label in TOP:
        section = in_flight and href == "flight-computer.html"
        items.append(f"<li>{link(href, label, current, section)}</li>")
    rows = f'<ul class="top">{"".join(items)}</ul>'
    if in_flight:
        kids = "".join(f"<li>{link(h, lab, current)}</li>" for h, lab in FLIGHT)
        rows += f'<ul class="sub">{kids}</ul>'
    return rows


def main():
    layout = (ROOT / "layout.html").read_text()
    OUT.mkdir(exist_ok=True)
    missing = []
    for name, title, description in PAGES:
        body = (ROOT / "content" / name).read_text().strip()
        for ref in re.findall(r'(?:src|href)="(images/[^"]+)"', body):
            if not (ROOT / ref).is_file():
                missing.append(f"{name}: {ref}")
        bare = re.findall(r"<img\b(?![^>]*\balt=)[^>]*>", body)
        if bare:
            sys.exit(f"{name} image without alt:\n" + "\n".join(bare))
        page = (
            layout.replace("{{title}}", escape(title))
            .replace("{{description}}", escape(description))
            .replace("{{canonical}}", escape(SITE + name))
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
    page_files = sorted(name for name, _, _ in PAGES)
    if content_files != page_files:
        sys.exit(f"content files {content_files} != pages {page_files}")
    if missing:
        sys.exit("missing images:\n" + "\n".join(missing))


if __name__ == "__main__":
    main()
