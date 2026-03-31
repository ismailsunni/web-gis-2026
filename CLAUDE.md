# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Web GIS course materials repository for a vocational program at UGM (Universitas Gadjah Mada), Indonesia. It contains week-by-week presentation slides (in Markdown) and hands-on demo applications.

**No build system, no package manager, no test framework.** All examples are plain HTML/JavaScript loaded via CDN.

## Running Examples

Open HTML files directly in a browser:
- `internet-programming/index.html` — Week 4 mini WebGIS demo (vanilla JS)
- `web-gis-development/index.html` — Week 7 OpenLayers demo
- `examples/index.html` — Minimal marker example

For presentations, the `.md` files are the source; `.pdf` and `.html` are exports.

## Repository Structure

Each week is a self-contained folder:
- `internet-programming/` — Week 4: JavaScript fundamentals, OOP, DOM manipulation, mini WebGIS without libraries
- `web-gis-development/` — Week 7: WebGIS architecture, maps API comparison, OpenLayers hands-on
- `examples/` — Simplified standalone examples

Each folder contains: `*.md` (presentation source), `index.html` (live demo), `app.js` (demo logic), and optional PDF exports.

## Architecture of Demo Applications

All demos follow a client-side-only pattern — no server required.

**Week 7 OpenLayers app (`web-gis-development/app.js`):**
- Coordinates stored as EPSG:4326 (lon/lat), converted to EPSG:3857 internally via `ol.proj.fromLonLat()`
- Three basemap tile layers (OSM, CARTO, Esri satellite) with a UI switcher
- Landmark data as an inline JSON array → rendered as a vector layer with category-based circle styles
- GeoJSON polygons for area zones
- Popup overlay system using `ol.Overlay` on map click

**Week 4 vanilla JS app (`internet-programming/app.js`):**
- Demonstrates OOP via a `Marker` class that creates DOM elements
- No mapping library — pure DOM manipulation for educational purposes

## Presentation Format

Presentations are written in Markdown and converted to slides (likely via Marp or a similar tool). When editing `.md` files, preserve slide separator conventions (`---`) and existing front matter if any.

## Technology Stack

- **OpenLayers 10.x** (CDN) — primary mapping library for examples
- **Leaflet** — covered in Week 5 (not in this repo's demos)
- **Vanilla JavaScript ES6+** — classes, arrow functions, template literals
- **No TypeScript, no bundler, no linter**
