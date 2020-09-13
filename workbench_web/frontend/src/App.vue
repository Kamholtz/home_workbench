<template>
    <div id="app">
        <div style="height: 50vh; width: inherit">
            <canvas id="myChart" ></canvas>
        </div>
        <v-app id="inspire">
            <v-container class="grey lighten-5">
                <v-row no-gutters>
                    <PowerSupplyCard
                        v-for="item in powersupplies"
                        v-bind:powersupply="item"
                        v-bind:key="item.id"
                    ></PowerSupplyCard>
                </v-row>
            </v-container>
        </v-app>
    </div>
</template>

<script>
import PowerSupplyCard from "./components/PowerSupplyCard.vue";
import PowerSupplyChart from "@/chart_helpers.js";

export default {
    name: "App",
    components: {
        PowerSupplyCard
    },
    data: function() {
        return {
            powersupplies: [
                {
                    id: 1,
                    voltage: 10,
                    state: "OFF",
                    text: "this is channel 1"
                },
                {
                    id: 2,
                    voltage: 3.3,
                    state: "OFF",
                    text: "this is channel 2"
                },
                {
                    id: 3,
                    voltage: 5,
                    state: "OFF",
                    text: "this is channel 3"
                }
            ]
        };
    },
    created: async function() {
        var thisRef = this;
        const gResponse = await fetch("http://localhost:5000/greeting");
        const gObject = await gResponse.json();
        console.log("greeting: " + gObject.greeting);
        this.flaskGreeting = gObject.greeting;

        // https://markus.oberlehner.net/blog/distributed-vue-applications-pushing-content-and-component-updates-to-the-client/

        const channelStatusWs = new WebSocket("ws://localhost:5000/channelstatus");
        channelStatusWs.onmessage = function (event) {
            const status = JSON.parse(event.data);
            thisRef.updatePowerSupplyCards(status);
            console.log("channelStatusWs.onmessage -> status", status);
        };
    },
    methods: {
        updatePowerSupplyCards(statusData) {
            this.powersupplies[0].state = statusData[0].state == 0 ? "OFF" : "ON"
            this.powersupplies[1].state = statusData[1].state == 0 ? "OFF" : "ON"
        }
    }
};

window.onload = function() {
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
