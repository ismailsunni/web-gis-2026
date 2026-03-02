---
marp: true
theme: default
paginate: true
size: 16:9
---

# Client-Side Programming in WebGIS
## From Markup to Interactive Architecture

Ismail Sunni
Geospatial Software Engineer
Camptocamp DE

---

# Ismail Sunni

- Jump into open source geospatial in 2012
- Developing almost all GIS application (library, desktop, web, etc...)
- Currently working for Camptocamp DE
- [ismailsunni.id](ismailsunni.id)
- [github.com/ismailsunni](github.com/ismailsunni)

---

# Learning Objectives

By the end of this session, you should be able to:

- Explain the role of JavaScript in WebGIS
- Understand DOM manipulation
- Understand event-driven systems
- Explain why OOP is important in WebGIS
- Build a simple interactive mini WebGIS

---
<!--
# Opening Question

- Is WebGIS just a map inside a browser?
- If we remove JavaScript, is it still WebGIS?
- What makes a map interactive?

Discuss in chat.

--- -->

# WebGIS Architecture Overview

Client Side:
- HTML (Structure)
- CSS (Style)
- JavaScript (Logic)
- GIS Library (Leaflet / OpenLayers)

Server Side:
- Database
- Spatial API
- GeoServer

Today: Focus on **Client-Side Logic**

---

# Without JavaScript

HTML only:

- Static layout
- No interaction
- No dynamic update

With JavaScript:

- Zoom
- Click events
- Add/remove layers
- Popups

JavaScript makes WebGIS alive.

---

# JavaScript Refresher
## Variables in GIS Context

```javascript
let layerName = "Roads";
let featureCount = 120;
let isVisible = true;
```

Why are data types important in spatial systems?

- Coordinates must be numbers
- Attributes may be strings
- Visibility is boolean

---

# Functions = Actions in GIS

```javascript
function toggleLayer() {
    console.log("Layer toggled");
}
```

In WebGIS:

- zoomIn()
- zoomOut()
- addLayer()
- removeLayer()

Function = behavior of the system.

---

# Object = Spatial Entity Representation

```javascript
let layer = {
    name: "Roads",
    visible: false
};
```

Another example:

```javascript
let marker = {
    lat: -7.5,
    lng: 110.3
};
```

WebGIS = Collection of interacting objects.

---

# Why Objects Matter

In GIS we have:

- Map
- Layer
- Marker
- Feature
- Control

Each has:

- Properties
- Behaviors

That is Object-Oriented Thinking.

---

# DOM (Document Object Model)

Browser transforms HTML into objects.

HTML:

```html
<div id="map"></div>
```

JavaScript:

```javascript
document.getElementById("map");
```

DOM = HTML represented as programmable objects.

---

# Why DOM is Critical in WebGIS

Because:

- The map is rendered inside a `<div>`
- Markers are DOM elements
- Popups are dynamic elements

Without DOM manipulation → no interactivity.

---

# Event-Driven System

WebGIS reacts to user actions:

- Click
- Zoom
- Drag
- Hover

Structure:

User Action
→ Event
→ Function
→ Update UI

---

# Example: Event Listener

```javascript
document
  .getElementById("btnLayer")
  .addEventListener("click", function() {
      alert("Layer activated");
  });
```

Event → Listener → Action

---

# Why OOP in WebGIS?

Imagine 10 layers:

Without structure → messy code
With OOP → clean architecture

We need:

- Blueprint
- Instances
- Encapsulation

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
```

---

# Creating Instances

```javascript
let roadLayer = new Layer("Roads");
let riverLayer = new Layer("Rivers");

roadLayer.toggle();
```

Each layer becomes an independent object.

---

# Mental Model

WebGIS =

- Objects
- Events
- DOM Manipulation
- Rendering Engine

Library (Leaflet) only wraps these concepts.

---

# Live Coding Project
## Mini WebGIS (Without Library)

Goal:

Understand the architecture before using Leaflet.

---

# Step 1 — Basic HTML

```html
<!DOCTYPE html>
<html>
<head>
    <title>Mini WebGIS</title>
    <style>
        #map {
            width: 100%;
            height: 400px;
            background-color: lightblue;
            position: relative;
        }

        .marker {
            width: 10px;
            height: 10px;
            background: red;
            position: absolute;
            border-radius: 50%;
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

# Step 2 — JavaScript Logic

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
});
```

---

# What Just Happened?

We performed:

- DOM creation
- Event handling
- Object generation
- Dynamic rendering

This simulates how GIS libraries work internally.

---

# Upgrade: Add Click Event to Marker

```javascript
marker.addEventListener("click", function() {
    alert("This is a marker");
});
```

Now we have nested events.

---

# Upgrade: Using OOP for Marker

```javascript
class Marker {
    constructor(x, y) {
        this.element = document.createElement("div");
        this.element.className = "marker";
        this.element.style.left = x + "px";
        this.element.style.top = y + "px";
    }

    addTo(map) {
        map.appendChild(this.element);
    }
}
```

---

# Using the Marker Class

```javascript
let m = new Marker(100, 150);
m.addTo(map);
```

Now we think architecturally.

---

# Reflection Questions

- Why is WebGIS event-driven?
- Why is everything modeled as objects?
- What problem does OOP solve?
- What do GIS libraries abstract away?

---

# Key Takeaways

- WebGIS is not just HTML
- JavaScript controls interaction
- DOM enables rendering
- Events drive behavior
- OOP structures complexity

---

# Next Session

We will use:

- Leaflet
- Real spatial layers
- GeoJSON
- Layer control

Today → Understanding the engine
Next → Using the engine

---

# Mini Assignment

Modify the project:

- Add 3 different marker colors
- Add "Clear All Markers" button
- Convert marker logic fully into class
- Add simple layer visibility toggle

---

# Final Thought

JavaScript in WebGIS is not about syntax.

It is about:

Interactive Spatial System Architecture.
