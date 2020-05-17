<script>
import { Bar, mixins } from 'vue-chartjs';

export default {
  name: "BarChart",
  extends: Bar,
  props: [
    'height',
    'width',
    'chartData',
  ],
  mounted() {
    this.renderChart(this.chartData, {
      responsive: false,
      maintainAspectRatio: false,
    });
  },
  watch: {
    chartData: function(New, Old) {
      this.renderChart(New, {
        responsive: false,
        maintainAspectRatio: false,
      });
    },
  }
}
</script>
