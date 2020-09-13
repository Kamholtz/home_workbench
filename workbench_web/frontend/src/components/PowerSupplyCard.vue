<template>
  <v-col cols="12" sm="6">
      <v-card class="mx-auto" max-width="344" outlined>
          <v-list-item three-line>
              <v-list-item-content>
                  <div class="overline mb-4">Channel {{ powersupply.id }}</div>
                  <v-list-item-title class="headline mb-1">State: {{ powersupply.state }}</v-list-item-title>
                  <v-list-item-subtitle>Source Voltage: {{ powersupply.voltage }} V</v-list-item-subtitle>
                  <v-list-item-subtitle>Source Current: {{ powersupply.current }} A</v-list-item-subtitle>
              </v-list-item-content>
          </v-list-item>

          <v-card-actions>
              <v-btn text>Enable</v-btn>
              <v-btn text>Disable</v-btn>
          </v-card-actions>
      </v-card>
  </v-col>
</template>

<script>
export default {
  name: "PowerSupplyCard",
  props: {
    powersupply: Object
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
