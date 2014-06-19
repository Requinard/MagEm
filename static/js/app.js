$(".status-circle").click(function (e) {
	var clickx = e.originalEvent.layerX - 50;
	var clicky = (e.originalEvent.layerY - 50) * -1;

	var angle = Math.atan2(clickx, clicky) * (180 / Math.PI);

	if (clickx < 0) {
		angle = 180 + (180 + angle)
	}

	var con = false;
	var agr = false;

	if (angle > 315 || angle <= 45) {
		con = true;
		agr = true;
	}
	else if (45 < angle <= 135) {
		agr = true;
	}
	else if (225 < angle <= 315) {
		con = true;
	}

	var item = this.attributes["article"].value;
	var mag = this.attributes["mag"].value;

	var payload = {
		"article": item,
		"mag": mag,
		"constructive": con.toString(),
		"agree": agr.toString(),
		"user": (1).toString()
	}

	$.post("/api/vote/", payload, function (response) {
		console.log(response)
	})
});