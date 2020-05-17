<template>
  <div style="text-align:center">
    <h5>{{ suburb }}</h5>
    <div class="prompt" style="display:flex">
      <pie-chart :height="250" :width="250" :name="name[0]" :chart-data="data[0]"></pie-chart>
      <pie-chart :height="250" :width="250" :name="name[1]" :chart-data="data[1]"></pie-chart>
    </div>
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
        'suburb',
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