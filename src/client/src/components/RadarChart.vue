<script>
import { Radar } from 'vue-chartjs';
 
export default {
  name: "RadarChart",
  extends: Radar,
  props: [
    'chartData',
  ],
  mounted() {
    this.renderChart({
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
      datasets: [
        {
          label: 'GitHub Commits',
          backgroundColor: '#666',
          data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11],
        },
      ],
    });
  },
}
</script>
