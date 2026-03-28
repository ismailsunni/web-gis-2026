let map = document.getElementById("map");

class Marker {
  constructor(x, y) {
    this.element = document.createElement("div");
    this.element.className = "marker";
    this.element.style.left = x + "px";
    this.element.style.top = y + "px";
    this.element.addEventListener("click", () => this.onClick());
  }
  onClick() {
    alert("Marker at " + this.element.style.left);
  }
  addTo(map) {
    map.appendChild(this.element);
  }
}

document.getElementById("btnAdd").addEventListener("click", function () {
  let marker = new Marker(
    Math.random() * map.clientWidth,
    Math.random() * map.clientHeight,
  );
  marker.addTo(map);
});
