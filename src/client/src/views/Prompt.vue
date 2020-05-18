<template>
  <div style="text-align:center">
    <h5>{{ suburb }}</h5>
    <div class="prompt" style="display:flex">
      <pie-chart :height="250" :width="250" :name="name[0]" :chart-data="data[0]" :options="options"></pie-chart>
      <pie-chart :height="250" :width="250" :name="name[1]" :chart-data="data[1]" :options="options"></pie-chart>
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
    data() {
      return {
        options: {
          tooltips: {
            callbacks: {
                label: function(tooltipItem, data) {
                    var label = data.labels[tooltipItem.index] || '';
                    if (label) {
                        label += ': ';
                    }
                    label += Math.round(data.datasets[0].data[tooltipItem.index] * 100) / 100;
                    label += '%';
                    return label;
                }
            }
          }
        }
      }
    },
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