---
marp: true
theme: default
paginate: true
size: 16:9
author: Ismail Sunni
date: March 2, 2026
---

# Client-Side Programming in WebGIS
## From Markup to Interactive Architecture

**Ismail Sunni** | Geospatial Software Engineer | Camptocamp DE

---

# About Me

- 🌍 Open source geospatial since 2012
- 🛠️ Full-stack GIS development (library, desktop, web, etc.)
- 💼 Currently @ Camptocamp DE
- 🔗 [ismailsunni.id](https://ismailsunni.id) | [github.com/ismailsunni](https://github.com/ismailsunni)

---

# Learning Objectives

By the end of this session, you should be able to:

✅ Explain the role of **JavaScript in WebGIS**
✅ Understand **DOM manipulation**
✅ Understand **event-driven systems**
✅ Explain why **OOP is important in WebGIS**
✅ Build a **simple interactive mini WebGIS**

---

# WebGIS Architecture Overview

## Client Side
- **HTML** — Structure
- **CSS** — Style
- **JavaScript** — Logic & Interaction
- **GIS Library** — Leaflet / OpenLayers

## Server Side
- Database & Spatial API
- GeoServer

---

## Focus: Client-Side Logic

---

# The Power of JavaScript

| Without JavaScript | With JavaScript |
|---|---|
| Static layout | Zoom & pan |
| No interaction | Click events |
| No dynamic updates | Add/remove layers |
| | Popups & feedback |

**JavaScript makes WebGIS alive.**

---

# JavaScript Fundamentals for GIS

## Variables in Spatial Context

```javascript
let layerName = "Roads";
let featureCount = 120;
let isVisible = true;
```

**Why types matter:** Coordinates must be numbers, attributes are strings, visibility is boolean.

---

# Functions = System Behavior

```javascript
function toggleLayer() {
    console.log("Layer toggled");
}
```

Common GIS functions:
- `zoomIn()` | `zoomOut()`
- `addLayer()` | `removeLayer()`
- `panTo()`

---

# Objects = Spatial Entities

```javascript
let layer = {
    name: "Roads",
    visible: false
};

let marker = {
    lat: -7.5,
    lng: 110.3
};
```

**WebGIS = collection of interacting objects**

---

# Why OOP Matters in GIS

Spatial systems have complexity:
- Map, Layer, Marker, Feature, Control
- Each has **properties** and **behaviors**

**Problem:** Managing 10+ layers without structure → chaos

**Solution:** Object-Oriented Design

---

# Why DOM is Critical

Because the map lives in a `<div>`, and everything is manipulated dynamically:
- Markers are DOM elements
- Popups appear/disappear
- Layers are toggled on/off

**Without DOM manipulation → no interactivity**

---

# Event-Driven Architecture

WebGIS reacts to user actions:

```
User Action → Event → Event Listener → Function → DOM Update
```

Examples: click, zoom, drag, hover

---

# Event Listener Example

```javascript
document
  .getElementById("btnLayer")
  .addEventListener("click", function() {
      toggleLayer();
  });
```

---

# Class as Blueprint

```javascript
class Layer {
    constructor(name) {
        this.name = name;
        this.visible = false;
    }

    toggle() {
        this.visible = !this.visible;
    }
}

let roadLayer = new Layer("Roads");
roadLayer.toggle();
```

---

# DOM (Document Object Model)

Browser transforms HTML into programmable objects.

```html
<!-- HTML -->
<div id="map"></div>
```

```javascript
// JavaScript
document.getElementById("map");
```

**DOM = HTML as interactive objects**

---

# 🔨 Live Coding: Mini WebGIS

Build a simple interactive map **without libraries** to understand the architecture.

---

# Step 1: HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
    <title>Mini WebGIS</title>
    <style>
        #map {
            width: 100%;
            height: 400px;
            background: linear-gradient(to bottom, lightblue, lightgreen);
            position: relative;
            border: 1px solid #ccc;
        }
        .marker {
            width: 12px;
            height: 12px;
            background: red;
            position: absolute;
            border-radius: 50%;
            cursor: pointer;
        }
    </style>
</head>
<body>
<h2>Mini WebGIS</h2>
<button id="btnAdd">Add Marker</button>
<div id="map"></div>
<script src="app.js"></script>
</body>
</html>
```

---

# Step 2: JavaScript Logic

```javascript
let map = document.getElementById("map");

document
  .getElementById("btnAdd")
  .addEventListener("click", function() {
    let marker = document.createElement("div");
    marker.className = "marker";

    marker.style.left = Math.random() * 380 + "px";
    marker.style.top = Math.random() * 380 + "px";

    map.appendChild(marker);

    marker.addEventListener("click", function() {
        alert("Marker clicked!");
    });
});
```

---

# What We Demonstrated

✅ DOM creation
✅ Event handling
✅ Object generation
✅ Dynamic rendering

**This is how GIS libraries work internally!**

---

# Step 3: OOP Refactor

```javascript
class Marker {
    constructor(x, y) {
        this.element = document.createElement("div");
        this.element.className = "marker";
        this.element.style.left = x + "px";
        this.element.style.top = y + "px";
        this.element.addEventListener("click",
            () => this.onClick());
    }

    onClick() {
        alert("Marker at " + this.element.style.left);
    }

    addTo(map) {
        map.appendChild(this.element);
    }
}
```

---

# Using the Class

```javascript
let m1 = new Marker(100, 150);
let m2 = new Marker(200, 250);

m1.addTo(map);
m2.addTo(map);
```

**Now we think architecturally.**

---

# Reflection

🤔 Why is WebGIS event-driven?
🤔 Why is everything modeled as objects?
🤔 What problem does OOP solve?
🤔 What do GIS libraries abstract away?

---

# Key Takeaways

1. WebGIS ≠ just HTML
2. JavaScript controls **all interaction**
3. DOM enables **dynamic rendering**
4. Events **drive behavior**
5. OOP **structures complexity**

---

# Next Session

We will use:
- **Leaflet** library
- **Real spatial layers**
- **GeoJSON data**
- **Layer control UI**

---

## Today → Understanding the engine
## Next → Using the engine

---

# 📋 Mini Assignment

Extend your project:

1. Add **3 different marker colors** (use a marker type parameter)
2. Add a **"Clear All Markers"** button
3. Refactor marker logic fully into a class
4. Add a **simple layer visibility toggle**

---

# Final Thought

JavaScript in WebGIS is **not about syntax**.

It is about:

## **Interactive Spatial System Architecture**
