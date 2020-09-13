'use strict';
var Chart = require('chart.js');
export default PowerSupplyChart

window.chartColors = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};


// function newDate(days) {
// 	return moment().add(days, 'd').toDate();
// }

// function newDateString(days) {
// 	return moment().add(days, 'd').format();
// }


// const MeasurementTypes = {
// 	Voltage: 1,
// 	Current: 2
// };

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
				data: []
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
			maintainAspectRatio: false,
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
			},
			plugins: {
				zoom: {
					// Container for pan options
					pan: {
						// Boolean to enable panning
						enabled: true,

						// Panning directions. Remove the appropriate direction to disable
						// Eg. 'y' would only allow panning in the y direction
						// A function that is called as the user is panning and returns the
						// available directions can also be used:
						//   mode: function({ chart }) {
						//     return 'xy';
						//   },
						mode: 'xy',

						rangeMin: {
							// Format of min pan range depends on scale type
							x: null,
							y: null
						},
						rangeMax: {
							// Format of max pan range depends on scale type
							x: null,
							y: null
						},

						// On category scale, factor of pan velocity
						speed: 20,

						// Minimal pan distance required before actually applying pan
						threshold: 10,

						// Function called while the user is panning
						onPan: function ({ chart }) { console.log(`I'm panning!!! ${chart}`); },
						// Function called once panning is completed
						onPanComplete: function ({ chart }) { console.log(`I was panned!!! ${chart}`); }
					},

					// Container for zoom options
					zoom: {
						// Boolean to enable zooming
						enabled: true,

						// Enable drag-to-zoom behavior
						drag: false,

						// Drag-to-zoom effect can be customized
						// drag: {
						// 	 borderColor: 'rgba(225,225,225,0.3)'
						// 	 borderWidth: 5,
						// 	 backgroundColor: 'rgb(225,225,225)',
						// 	 animationDuration: 0
						// },

						// Zooming directions. Remove the appropriate direction to disable
						// Eg. 'y' would only allow zooming in the y direction
						// A function that is called as the user is zooming and returns the
						// available directions can also be used:
						//   mode: function({ chart }) {
						//     return 'xy';
						//   },
						mode: 'xy',

						rangeMin: {
							// Format of min zoom range depends on scale type
							x: null,
							y: null
						},
						rangeMax: {
							// Format of max zoom range depends on scale type
							x: null,
							y: null
						},

						// Speed of zoom via mouse wheel
						// (percentage of zoom on a wheel event)
						speed: 0.1,

						// Minimal zoom distance required before actually applying zoom
						threshold: 2,

						// On category scale, minimal zoom level before actually applying zoom
						sensitivity: 3,

						// Function called while the user is zooming
						onZoom: function ({ chart }) { console.log(`I'm zooming!!! ${chart}`); },
						// Function called once zooming is completed
						onZoomComplete: function ({ chart }) { console.log(`I was zoomed!!! ${chart}`); }
					}
				}
			}
		}
	};

	this.chart = null;
}

PowerSupplyChart.prototype.Bind = function () {
	var thisRef = this;
	thisRef.chart = new Chart(thisRef.ctx, thisRef.config);

	const ws = new WebSocket("ws://localhost:5000/measurements");
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
