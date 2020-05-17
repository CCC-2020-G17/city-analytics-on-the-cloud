<template>
  <div style="display: flex; justify-content: center; flex-direction: column;align-items: center; overflow-x: auto;">
        <h5>{{ title }}</h5>
        <bar-chart :height="height || '550px'" :width="width || '1600px'" :name="name" :chart-data="data" :options="options"></bar-chart>
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
        'height',
        'title',
        'options',
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