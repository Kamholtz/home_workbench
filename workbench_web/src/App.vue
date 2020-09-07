<template>
  <div id="app">
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

export default {
  name: "App",
  components: {
    PowerSupplyCard,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
