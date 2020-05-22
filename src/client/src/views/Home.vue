<template>
  <div class="hello">
    <Nav />
    <Map id="map" @setBarChartData="this.setBarChartData" @setAx="this.setAx"></Map>
    <div class="statistics__container">
      <Statistics class="statistics" id="statistics" :data="barChart" :title="'Suburb Level Analysis'" :options="options"></Statistics>
    </div>
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
      options: null,
      optionsWithOneAx: {
        scales: {
            yAxes: [{
                id: 'y1',
                ticks: {
                    callback: (label, index, labels) => {
                        return label + '%';
                    },
                },
            }]
        },
        tooltips: {
          callbacks: {
              label: function(tooltipItem) {
                  var label = tooltipItem.label || '';
                  if (label) {
                      label += ': ';
                  }
                  label += Math.round(tooltipItem.yLabel * 100) / 100;
                  label += '%';
                  return label;
              }
          }
        }
      },
      optionsWithTwoAx: {
          scales: {
            yAxes: [{
              id: 'y1',
              type: 'linear',
              position: 'left',
              ticks: {
                  callback: (label, index, labels) => {
                      return label + '%';
                  },
              },
            }, {
              id: 'y2',
              position: 'right',
            }]
          },
          tooltips: {
            callbacks: {
                label: function(tooltipItem) {
                    var label = tooltipItem.label || '';
                    if (label) {
                        label += ': ';
                    }
                    label += Math.round(tooltipItem.yLabel * 100) / 100;
                    return label;
                }
            }
          }
      },
      barChart: null,
      usePer: true,
    }
  },
  props: {
    msg: String,
  },
  mounted() {
    this.options = this.optionsWithOneAx;
  },
  methods: {
    setBarChartData(barChart) {
      this.barChart = barChart;
    },
    setAx(useTwoAx) {
      console.log(useTwoAx);
      this.options = useTwoAx ? this.optionsWithTwoAx : this.optionsWithOneAx;
    }
  } 
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.statistics__container {
  display: flex;
  justify-content: center;
  width: 100%;
  height: 100vh;
}
.statistics {

  
  
}
</style>
