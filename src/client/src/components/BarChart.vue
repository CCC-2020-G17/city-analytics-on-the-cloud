<script>
import { Bar, mixins } from 'vue-chartjs';

export default {
  name: "BarChart",
  extends: Bar,
  props: [
    'height',
    'width',
    'chartData',
    'options'
  ],
  mounted() {
    const options = this.options || {};
    this.renderChart(this.chartData, {
      ...options,
      responsive: false,
      maintainAspectRatio: false,
      IsStaggered: true,
    });
  },
  watch: {
    chartData: function(New, Old) {
      const options = this.options || {};
      this.renderChart(New, {
        ...options,
        responsive: false,
        maintainAspectRatio: false,
        IsStaggered: true,
      });
    },
  }
}
</script>
