<template>
  <div class="prompt" style="text-align:center;display:flex">
    <pie-chart :height="250" :width="250" :name="name[0]" :chart-data="data[0]"></pie-chart>
    <pie-chart :height="250" :width="250" :name="name[1]" :chart-data="data[1]"></pie-chart>
  </div>
</template>

<script>
import PieChart from '../components/PieChart';
export default {
    name: 'prompt',
    components: {
      'pie-chart': PieChart
    },
    props: [
        'name',
        'data',
    ],
    mounted() {
      console.log(this.data);
    }
}
</script>

<style scoped>
span {
  font-size: 12px;
}
</style>