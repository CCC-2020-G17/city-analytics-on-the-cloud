<template>
  <div class="hello">
    <Nav />
    <Map id="map" @setBarChartData="this.setBarChartData"></Map>
    <Statistics class="statistics" id="statistics" :data="barChart"></Statistics>
  </div>
</template>

<script>
import Map from './Map.vue';
import Statistics from './Statistics.vue';
import Nav from '../components/Nav.vue';
export default {
  name: 'Home',
  components: {
    Map,
    Statistics,
    Nav,
  },
  data() {
    return {
      barChart: null,
    }
  },
  props: {
    msg: String
  },
  methods: {
    setBarChartData(barChart) {
      this.barChart = barChart;
      console.log(barChart);
    }
  } 
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.statistics {
  width: 100%;
  height: 100vh;
}
</style>
