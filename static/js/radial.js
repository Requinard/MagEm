/*
 SOURCE
 http://creative-punch.net/2014/02/making-animated-radial-menu-css3-javascript/
 */

function showchildren(selector) {
	var items = document.querySelectorAll(selector + ' a');


	for (var i = 0, l = items.length; i < l; i++) {
		items[i].style.left = (65 - 15 * Math.cos(-0.25 * Math.PI - 2 * (1 / l) * i * Math.PI)).toFixed(4) + "%";

		items[i].style.top = (80 + 25 * Math.sin(-0.25 * Math.PI - 2 * (1 / l) * i * Math.PI)).toFixed(4) + "%";
	}
	document.querySelector(selector).classList.toggle('open');
}