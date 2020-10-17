<template>
  <div id="app">
    <v-app id="inspire">
      <v-card>
        <v-tabs v-model="tab" align-with-title>
          <v-tab>Power Supply</v-tab>
          <v-tab>Solar Monitor</v-tab>
        </v-tabs>
      </v-card>

      <v-tabs-items v-model="tab">
        <v-tab-item>
          <v-card flat>
            <div style="height: 50vh; width: inherit">
              <canvas id="myChart"></canvas>
            </div>
            <v-container class="grey lighten-5">
              <v-row no-gutters>
                <PowerSupplyCard
                  v-for="item in powersupplies"
                  v-bind:powersupply="item"
                  v-bind:key="item.id"
                ></PowerSupplyCard>
              </v-row>
            </v-container>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card flat>
            <div style="height: 75vh; width: inherit">
              <SolarMonitorChart
                :chart-data="solarchartdata"
                :options="solarchartoptions"
              >
              </SolarMonitorChart>
            </div>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-app>
  </div>
</template>

<script>
import PowerSupplyCard from "./components/PowerSupplyCard.vue";
import SolarMonitorChart from "./components/SolarMonitorChart.vue";
import PowerSupplyChart from "@/chart_helpers.js";

export default {
  name: "App",
  components: {
    PowerSupplyCard,
    SolarMonitorChart,
  },
  data: function () {
    return {
      tab: null,
      powersupplies: [
        {
          id: 1,
          voltage: "?",
          current: "?",
          state: "???",
        },
        {
          id: 2,
          voltage: "?",
          current: "?",
          state: "???",
        },
      ],
      solarchartdata: {},
      solarchartoptions: {
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          text: "Solar Monitor",
        },
        scales: {
          xAxes: [
            {
              type: "time",
              display: true,
              scaleLabel: {
                display: true,
                labelString: "Date",
              },
              ticks: {
                major: {
                  fontStyle: "bold",
                  fontColor: "#FF0000",
                },
                time: {
                  unit: "second",
                },
              },
            },
          ],
          yAxes: [
            {
              display: true,
              position: "left",
              scaleLabel: {
                display: true,
                labelString: "Voltage (V)",
              },
              id: "y-axis-voltage",
            },
            {
              display: true,
              position: "right",
              scaleLabel: {
                display: true,
                labelString: "Current (A)",
              },
              ticks: {
                suggestedMax: 0.2,
              },
              id: "y-axis-current",
            },
          ],
        },
      },
    };
  },
  created: async function () {
    var thisRef = this;

    // https://markus.oberlehner.net/blog/distributed-vue-applications-pushing-content-and-component-updates-to-the-client/

    const channelStatusWs = new WebSocket(
      "ws://192.168.1.15:5000/channelstatus"
    );
    channelStatusWs.onmessage = function (event) {
      const status = JSON.parse(event.data);
      thisRef.updatePowerSupplyCards(status);
      console.log("channelStatusWs.onmessage -> status", status);
    };
  },
  methods: {
    updatePowerSupplyCards(statusData) {
      this.powersupplies[0].state = statusData[0].state == 0 ? "OFF" : "ON";
      this.powersupplies[0].voltage = statusData[0].voltage;
      this.powersupplies[0].current = statusData[0].current;

      this.powersupplies[1].state = statusData[1].state == 0 ? "OFF" : "ON";
      this.powersupplies[1].voltage = statusData[1].voltage;
      this.powersupplies[1].current = statusData[1].current;
    },
    initSolarChartData() {
      this.solarchartdata = {
        datasets: [
          {
            label: "Voltage",
            backgroundColor: "orange",
            borderColor: "orange",
            fill: false,
            data: [],
          },
        ],
      };
    },
  },
  mounted() {
    var thisRef = this;
    this.initSolarChartData();

    const solarMeasurementsWs = new WebSocket(
      "ws://192.168.1.15:5000/solarmeasurements"
    );
    solarMeasurementsWs.onmessage = function (event) {
      const measurements = JSON.parse(event.data);
      console.log("solarMeasurementsWs.onmessage -> status", measurements);

      measurements.forEach((m) => {
        var data = {
          x: m.time,
          y: m.value,
        };

        thisRef.solarchartdata.datasets[m.measurement_type - 1].data.push(data);
      });
    };
  },
};

window.onload = function () {
  var powerSupplyChart = new PowerSupplyChart();
  powerSupplyChart.ctx = document.getElementById("myChart").getContext("2d");
  powerSupplyChart.Bind();
};
</script>

<style>
#myChart {
  min-height: 319px;
}
</style>
