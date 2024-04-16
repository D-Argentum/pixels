const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
let coord = { x: 0, y: 0 };

document.addEventListener("mousedown", start);
document.addEventListener("mouseup", stop);
window.addEventListener("resize", resize);

function resize() {
  ctx.canvas.width = 28;
  ctx.canvas.height = 28;
}

resize();

function start(event) {
  document.addEventListener("mousemove", draw);
  reposition(event);
}

function reposition(event) {
  coord.x = event.clientX - canvas.offsetLeft;
  coord.y = event.clientY - canvas.offsetTop;
}

function stop() {
  document.removeEventListener("mousemove", draw);
  var pixels = [];
  for (var x = 0; x < 28; x++) {
    for (var y = 0; y < 28; y++) {
      var imgData = ctx.getImageData(y, x, 1, 1);
      var data = imgData.data;
      //Pixel negro o blanco?
      var color = data[3] / 255; //Data tiene 4 canales:Rojo, Verde, Azul, Alpha
      //Divido entre 255 para tener de 0 a 1
      //Dejar siempre 2 decimales
      color = (Math.round(color * 100) / 100).toFixed(2);
      pixels.push(color);
    }
  }
  $.post(
    "http://localhost:8000",
    { pixeles: pixels.join(",") },
    function (response) {
      console.log("Resultado: " + response);
      $("#resultado").html(response);
    }
  );
}

function draw(event) {
  ctx.beginPath();
  ctx.lineWidth = 1;
  ctx.lineCap = "round";
  ctx.strokeStyle = "#black";
  ctx.moveTo(coord.x, coord.y);
  reposition(event);
  ctx.lineTo(coord.x, coord.y);
  ctx.stroke();
}
