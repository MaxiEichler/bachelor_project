document.addEventListener("DOMContentLoaded", () => {

  const svg = document.getElementById("breadboard");
  const toggle = document.getElementById("routingToggle");
  const routingLabel = document.getElementById("routinglabel");

  let firstSelected = null;

  /* Breadboard grid */
  const cols = 16, rows = 10, spacingx = 20, spacingy = 20, extraGap = 20;

  /* Column labels */
  for (let c = 0; c < cols; c++) {
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");

    text.setAttribute("x", 50 + c * spacingx);
    text.setAttribute("y", 35);  // position above first row
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("font-size", "12");
    text.setAttribute("fill", "#333");

    text.textContent = c + 1; // column number (1–16)

    svg.appendChild(text);
  }

  /* Create holes */
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


    const isDataLane = toggle.checked;
    const lineColor = isDataLane ? "blue" : "red";  
    // blue = data, red = power (change if you prefer)
  
    /* If this is the first hole, just select it. If it's the second, draw a line and reset. */
    if (!firstSelected) {
      firstSelected = hole;
    } else {
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", firstSelected.getAttribute("cx"));
      line.setAttribute("y1", firstSelected.getAttribute("cy"));
      line.setAttribute("x2", hole.getAttribute("cx"));
      line.setAttribute("y2", hole.getAttribute("cy"));
      line.setAttribute("stroke", lineColor);
      line.setAttribute("stroke-width", "2");
      svg.appendChild(line);

        document.getElementById('xlabel1').innerText = 'X1: ' + firstSelected.getAttribute('cx');
        document.getElementById('ylabel1').innerText = 'Y1: ' + firstSelected.getAttribute('cy');
        document.getElementById('xlabel2').innerText = 'X2: ' + hole.getAttribute('cx');
        document.getElementById('ylabel2').innerText = 'Y2: ' + hole.getAttribute('cy');

      /* send x1, y1, x2 and y2 to python script */
      fetch("/send-coordinates", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          x1: firstSelected.getAttribute("cx"),
          y1: firstSelected.getAttribute("cy"),
          x2: hole.getAttribute("cx"),
          y2: hole.getAttribute("cy"),
          routeType: isDataLane ? "data" : "power"
        })
      })
      .then(response => response.json())
      .then(data => {
        console.log("Server result:", data.result);
      });

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

  /* Reset button */
  document.getElementById("clearBtn").addEventListener("click", () => {
    // Remove all lines
    const lines = svg.querySelectorAll("line");
    lines.forEach(line => line.remove());
    // Reset all holes
    const holes = svg.querySelectorAll("circle");
    holes.forEach(hole => hole.setAttribute("fill", "#eee"));
    firstSelected = null;
  });

  /* Remove last Route */
  document.getElementById("removelast").addEventListener("click", () => {

    const lines = svg.querySelectorAll("line");

    if (lines.length > 0) {
      const lastLine = lines[lines.length - 1];

      // Optionally grab its coordinates before removing
      const x1 = lastLine.getAttribute("x1");
      const y1 = lastLine.getAttribute("y1");
      const x2 = lastLine.getAttribute("x2");
      const y2 = lastLine.getAttribute("y2");

      lastLine.remove();

      // Send coordinates of removed line to backend
      fetch("/remove-route", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ x1, y1, x2, y2 })
      })
      .then(response => response.json())
      .then(data => {
        console.log("Remove route result:", data.result);
      });
    }

    firstSelected = null;
  });
});
