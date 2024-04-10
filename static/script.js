
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var drawing = false;

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', endDrawing);
canvas.addEventListener('mouseout', endDrawing);

function startDrawing(e) {
    drawing = true;
    draw(e);
}

function draw(e) {
    if (!drawing) return;
    ctx.lineWidth = 10;
    ctx.lineCap = 'round';
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.offsetX, e.offsetY);


    var pixels = [];
        for (var x=0; x < 28; x++) {
            for (var y=0; y < 28; y++) {
                var imgData = ctx.getImageData(y,x,1,1);
                var data = imgData.data;
                //Pixel negro o blanco?
                var color = (data[3])/255; //Data tiene 4 canales:Rojo, Verde, Azul, Alpha
                //Dejar siempre 2 decimales
                //Divido entre 255 para tener de 0 a 1
                color = (Math.round(color*100)/100).toFixed(2)
                pixels.push(color);
                } }
}

function endDrawing() {
    drawing = false;
}

function sendDrawing() {
    var pixelData = pixels.join(",");
    $.post("http://localhost:8000", { pixels: pixelData }, function(response) {
        console.log("Resultado: " + response);
        alert('Prediction: ' + response.prediction);
    });
}
