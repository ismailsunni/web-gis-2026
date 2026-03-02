// Get map container
const map = document.getElementById("map");

// Store markers
let markers = [];

/* =========================
   MARKER CLASS (OOP)
========================= */

class Marker {
    constructor(x, y) {
        this.x = x;
        this.y = y;

        this.element = document.createElement("div");
        this.element.className = "marker";

        this.element.style.left = x + "px";
        this.element.style.top = y + "px";

        // Add click event
        this.element.addEventListener("click", () => {
            alert("Marker at X: " + this.x + ", Y: " + this.y);
        });
    }

    addTo(parent) {
        parent.appendChild(this.element);
    }

    remove() {
        this.element.remove();
    }
}

/* =========================
   ADD RANDOM MARKER
========================= */

document.getElementById("btnAdd").addEventListener("click", function () {

    const maxWidth = map.clientWidth - 15;
    const maxHeight = map.clientHeight - 15;

    const randomX = Math.random() * maxWidth;
    const randomY = Math.random() * maxHeight;

    const marker = new Marker(randomX, randomY);
    marker.addTo(map);

    markers.push(marker);
});

/* =========================
   CLEAR ALL MARKERS
========================= */

document.getElementById("btnClear").addEventListener("click", function () {

    markers.forEach(marker => marker.remove());
    markers = [];

});
