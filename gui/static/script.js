document.addEventListener("DOMContentLoaded", () => {

  const svg = document.getElementById("breadboard");
  const toggle = document.getElementById("routingToggle");
  const routingLabel = document.getElementById("routinglabel");

  let firstSelected = null;

  /* Breadboard grid */
  const cols = 17, rows = 10, spacingx = 20, spacingy = 20, extraGap = 20;

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      const yOffset = r >= 5 ? extraGap : 0;

      circle.setAttribute("cx", 50 + c * spacingx);
      circle.setAttribute("cy", 50 + r * spacingy + yOffset);
      circle.setAttribute("r", 5);
      circle.setAttribute("fill", "#eee");
      circle.setAttribute("stroke", "#999");
      circle.style.cursor = "pointer";

      svg.appendChild(circle);
    }
  }

  /* SVG click logic */
  svg.addEventListener("click", e => {
    if (e.target.tagName !== "circle") return;

    const hole = e.target;
    hole.setAttribute("fill", "#ff0");

    if (!firstSelected) {
      firstSelected = hole;
    } else {
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", firstSelected.getAttribute("cx"));
      line.setAttribute("y1", firstSelected.getAttribute("cy"));
      line.setAttribute("x2", hole.getAttribute("cx"));
      line.setAttribute("y2", hole.getAttribute("cy"));
      line.setAttribute("stroke", "red");
      line.setAttribute("stroke-width", "2");
      svg.appendChild(line);

        document.getElementById('xlabel1').innerText = 'X1: ' + firstSelected.getAttribute('cx');
        document.getElementById('ylabel1').innerText = 'Y1: ' + firstSelected.getAttribute('cy');
        document.getElementById('xlabel2').innerText = 'X2: ' + hole.getAttribute('cx');
        document.getElementById('ylabel2').innerText = 'Y2: ' + hole.getAttribute('cy');

      firstSelected.setAttribute("fill", "#eee");
      hole.setAttribute("fill", "#eee");
      firstSelected = null;
    }
  });

  /* Switch behavior */
  toggle.addEventListener("change", () => {
    routingLabel.textContent = toggle.checked
      ? "Routing Options: Datalane Two-Way"
      : "Routing Options: Powerlane One-Way";
  });

});
