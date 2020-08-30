'use strict';

window.chartColors = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};


function newDate(days) {
	return moment().add(days, 'd').toDate();
}

function newDateString(days) {
	return moment().add(days, 'd').format();
}


const MeasurementTypes = {
	Voltage: 1,
	Current: 2
};

function PowerSupplyChart() {
	this.ctx = null;

	// -------------------------
	this.color = Chart.helpers.color;

	this.config = {
		type: 'line',
		data: {
			datasets: [{
				label: 'Voltage',
				backgroundColor: this.color(window.chartColors.red).alpha(0.5).rgbString(),
				borderColor: window.chartColors.red,
				fill: false,
				data: [],
			}, {
				label: 'Current',
				backgroundColor: this.color(window.chartColors.blue).alpha(0.5).rgbString(),
				borderColor: window.chartColors.blue,
				fill: false,
				data: []
			}]
		},
		options: {
			responsive: true,
			title: {
				display: true,
				text: 'Power Supply'
			},
			scales: {
				xAxes: [{
					type: 'time',
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Date'
					},
					ticks: {
						major: {
							fontStyle: 'bold',
							fontColor: '#FF0000'
						},
						time: {
							unit: "second"
						}
					}
				}],
				yAxes: [{
					display: true,
					position: 'left',
					scaleLabel: {
						display: true,
						labelString: 'Voltage (V)'
					}
				},
				{
					display: true,
					position: 'right',
					scaleLabel: {
						display: true,
						labelString: 'Current (A)'
					},
					ticks: {
						suggestedMax: 0.2
					}
				}
				]
			}
		}
	};

	this.chart = null;
}

PowerSupplyChart.prototype.Bind = function () {
	var thisRef = this;
	thisRef.chart = new Chart(thisRef.ctx, thisRef.config);

	const ws = new WebSocket("ws://192.168.1.51:8000/ws");
	ws.onmessage = function (event) {
		const measurements = JSON.parse(event.data);

		measurements.forEach((m) => {
			var data = {
				x: m.time,
				y: m.value
			};

			thisRef.chart.data.datasets[m.measurement_type - 1].data.push(data);
		});

		thisRef.chart.update();
	};
}
