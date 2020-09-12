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
                    text: "this is channel 1"
                },
                {
                    id: 2,
                    voltage: 3.3,
                    text: "this is channel 2"
                },
                {
                    id: 3,
                    voltage: 5,
                    text: "this is channel 3"
                }
            ]
        };
    },
    created: async function() {
        const gResponse = await fetch("http://localhost:5000/greeting");
        const gObject = await gResponse.json();
        console.log("greeting: " + gObject.greeting);
        this.flaskGreeting = gObject.greeting;
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
