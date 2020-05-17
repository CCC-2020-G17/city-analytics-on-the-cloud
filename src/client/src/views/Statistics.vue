<template>
  <div style="display: flex; justify-content: center; align-items: center; overflow-x: auto;">
        <bar-chart :height="'550px'" :width="width || '2000px'" :name="name" :chart-data="data"></bar-chart>
  </div>
</template>

<script>
import BarChart from '../components/BarChart';
export default {
    name: 'statistics',
    components: {
      'bar-chart': BarChart
    },
    props: [
        'name',
        'data',
        'width',
    ],
    mounted() {
      console.log(this.data);
    },
}
</script>

<style scoped>
span {
  font-size: 12px;
}
</style>