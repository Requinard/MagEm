$(".status-circle").click(function (e) {
    var clickx = e.originalEvent.layerX - 50;
    var clicky = (e.originalEvent.layerY - 50) * -1;

    var angle = Math.abs(Math.atan(clickx / clicky) * (180 / Math.PI));

    console.log(angle)
});