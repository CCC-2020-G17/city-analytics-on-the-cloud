<template>
    <div class="front">
        <header id="header">
            <b-button @click="() => { this.$router.push('/map')}" class="more">Go To Map</b-button>
        </header>
        <div class="main">
            <div class="title">
                <h2 style="padding: 10px;">COMP90024 CLUSTER AND CLOUD COMPUTING</h2>
                <h4>Members:</h4>
                <h6>Yawei Sun</h6>
                <h6>Tingli Qiu</h6>
                <h6>RongbingShan</h6>
                <h6>Zhaofeng Qiu</h6>
                <h6>Aoqi Zuo</h6>
            </div>
        </div>
        <Statistics class="statistics" id="statistics" :data="barChart" :width="'800px'"></Statistics>
    </div>
</template>

<script>
import Statistics from './Statistics.vue';
import axios from 'axios';

const cityAPI = 'api/v2.0/analysis/city-level/all';

export default {
  name: 'Front',
  components: {
    Statistics,
  },
  data() {
    return {
      barChart: null,
    }
  },
  props: {
    msg: String
  },
  mounted() {
    axios.get(cityAPI).then((res) => {
        const data = res.data;
        let MelbourneList, SydneyList, AdelaideList, BrisbaneList = [];
        let temp = data['adelaide']['covid-19'];
        let total = temp['tweet_count'] || 1;
        AdelaideList = [ temp['english_count'] / total, temp['chinese_count'] / total,  temp['others_count'] / total ];
        temp = data['melbourne']['covid-19'];
        total = temp['tweet_count'] || 1;
        MelbourneList = [ temp['english_count'] / total, temp['chinese_count'] / total,  temp['others_count'] / total ];
        temp = data['brisbane']['covid-19'];
        total = temp['tweet_count'] || 1;
        BrisbaneList = [ temp['english_count'] / total, temp['chinese_count'] / total,  temp['others_count'] / total ];
        temp = data['sydney']['covid-19'];
        total = temp['tweet_count'] || 1;
        SydneyList = [ temp['english_count'] / total, temp['chinese_count'] / total,  temp['others_count'] / total ];
        
        this.barChart = {
            labels: ['English', 'Chinese', 'Others'],
            datasets: [
                {
                    label: 'Melbourne',
                    backgroundColor: '#6C7B88',
                    data: MelbourneList,
                },
                {
                    label: 'Sydney',
                    backgroundColor: '#0a1D30',
                    data: SydneyList,
                },
                {
                    label: 'Adelaide',
                    backgroundColor: '#DBE5F0',
                    data: AdelaideList,
                },
                {
                    label: 'Brisbane',
                    backgroundColor: '#486C82',
                    data: BrisbaneList,
                }
            ]
        }
    })
    
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.statistics {
    height: 100vh;
    width: 100%;
}
.main {
    background: url('../assets/city.jpg');
    background-size: 100% 100%;
    background-repeat: no-repeat no-repeat;
    color: white;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}
#header {
    position: fixed;
    height: 40px;
    width: 100%;
    z-index: 999;
    .more {
        position: absolute;
        top: 0;
        right: 0;
        margin: 10px;
    }
}
</style>
