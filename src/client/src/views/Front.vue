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
                <h6>Rongbing Shan</h6>
                <h6>Zhaofeng Qiu</h6>
                <h6>Aoqi Zuo</h6>
            </div>
        </div>
        <div class="footer">
            <h2>City Level Analysis</h2>
            <h4>Who Are More Likely to Tweet about COVID-19</h4>
            <Statistics id="statistics" :data="covData" :width="'800px'"></Statistics>
            <h4>Young People Tweeting Preferences</h4>
            <Statistics id="statistics" :data="youngData" :width="'800px'" :options="youngOptions"></Statistics>
            <h4>Tweeting Frequency and English Proficiency</h4>
            <Statistics id="statistics" :data="denData" :width="'800px'" :options="denOptions"></Statistics>
        </div>
    </div>
</template>

<script>
import Statistics from './Statistics.vue';
import axios from 'axios';
import { ROOT} from '../utils/Api';
const cityAPI = ROOT + 'api/v2.0/analysis/city-level/all';

export default {
  name: 'Front',
  components: {
    Statistics,
  },
  data() {
    return {
      covData: null,
      youngData: null,
      youngOptions: {
        scales: {
            yAxes: [{
                ticks: {
                    min: 0,
                    max: 100,
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
      denData: null,
      denOptions: {
        scales: {
            yAxes: [{
                id: 'y1',
                type: 'linear',
                position: 'left',
                ticks: {
                    min: 0,
                    max: 100,
                    callback: (label, index, labels) => {
                        return label + '%';
                    },
                },
            }, {
                id: 'y2',
                type: 'linear',
                position: 'right',
                
            }]
        },
        tooltips: {
            callbacks: {
                label: function(tooltipItem, data) {
                    var label = tooltipItem.label || '';
                    if (label) {
                        label += ': ';
                    }
                    label += Math.round(tooltipItem.yLabel * 100) / 100;
                    if(tooltipItem.datasetIndex == 1) {
                        label += '%';
                    }
                    return label;
                }
            }
        }
      },
      
    }
  },
  props: {
    msg: String
  },
  mounted() {
    axios.get(cityAPI).then((res) => {
        const data = res.data;
        let levelA, levelB, levelC;
        levelA = [];
        levelB = [];
        levelC = [];

        let temp = data['adelaide']['covid-19'];
        levelA.push(temp['followers_within_100']);
        levelB.push(temp['followers_100_to_500']);
        levelC.push(temp['followers_above_500']);

        temp = data['melbourne']['covid-19'];
        levelA.push(temp['followers_within_100']);
        levelB.push(temp['followers_100_to_500']);
        levelC.push(temp['followers_above_500']);

        temp = data['brisbane']['covid-19'];
        levelA.push(temp['followers_within_100']);
        levelB.push(temp['followers_100_to_500']);
        levelC.push(temp['followers_above_500']);

        temp = data['sydney']['covid-19'];
        levelA.push(temp['followers_within_100']);
        levelB.push(temp['followers_100_to_500']);
        levelC.push(temp['followers_above_500']);

        temp = data['perth']['covid-19'];
        levelA.push(temp['followers_within_100']);
        levelB.push(temp['followers_100_to_500']);
        levelC.push(temp['followers_above_500']);
        
        this.covData = {
            labels: ['Adelaide', 'Melbourne', 'Brisbane', 'Sydney', 'Perth'],
            datasets: [
                {
                    label: 'Posters who have #followers less than 100',
                    backgroundColor: '#6C7B88',
                    data: levelA,
                },
                {
                    label: 'Posters who have #followers between 100 and 500',
                    backgroundColor: '#0a1D30',
                    data: levelB,
                },
                {
                    label: 'Posters who have #followers above 500',
                    backgroundColor: '#DBE5F0',
                    data: levelC,
                },
            ]
        }

        levelA = [];
        levelB = [];
        levelC = [];

        let total_twitter = data['adelaide']['city_tweet_count'] || 1;
        temp = data['adelaide']['young_twitter_preference'];
        levelA.push(temp['night_tweets_count'] / total_twitter * 100);
        levelB.push(temp['tweet_with_geo_count'] / total_twitter * 100);
        levelC.push(temp['young_people_proportion']);

        total_twitter = data['melbourne']['city_tweet_count'] || 1;
        temp = data['melbourne']['young_twitter_preference'];
        levelA.push(temp['night_tweets_count'] / total_twitter * 100);
        levelB.push(temp['tweet_with_geo_count'] / total_twitter * 100);
        levelC.push(temp['young_people_proportion']);

        total_twitter = data['brisbane']['city_tweet_count'] || 1;
        temp = data['brisbane']['young_twitter_preference'];
        levelA.push(temp['night_tweets_count'] / total_twitter * 100);
        levelB.push(temp['tweet_with_geo_count'] / total_twitter * 100);
        levelC.push(temp['young_people_proportion']);

        total_twitter = data['sydney']['city_tweet_count'] || 1;
        temp = data['sydney']['young_twitter_preference'];
        levelA.push(temp['night_tweets_count'] / total_twitter * 100);
        levelB.push(temp['tweet_with_geo_count'] / total_twitter * 100);
        levelC.push(temp['young_people_proportion']);

        total_twitter = data['perth']['city_tweet_count'] || 1;
        temp = data['perth']['young_twitter_preference'];
        levelA.push(temp['night_tweets_count'] / total_twitter * 100);
        levelB.push(temp['tweet_with_geo_count'] / total_twitter * 100);
        levelC.push(temp['young_people_proportion']);

        this.youngData = {
            labels: ['Adelaide', 'Melbourne', 'Brisbane', 'Sydney', 'Perth'],
            datasets: [
                {
                    label: 'Proportion of tweets posted at night',
                    backgroundColor: '#6C7B88',
                    data: levelA,
                },
                {
                    label: 'Proportion of tweets posted with location labels',
                    backgroundColor: '#0a1D30',
                    data: levelB,
                },
                {
                    label: 'Proportion of young people',
                    backgroundColor: '#DBE5F0',
                    data: levelC,
                },
            ]
        }

        levelA = [];
        levelB = [];
        levelC = [];
        total_twitter = data['adelaide']['city_tweet_count'] || 1;
        temp = data['adelaide']['tweet_density'];
        levelA.push(total_twitter / temp['unique_user_count']);
        levelB.push(temp['english_mother_tongue_proportion']);
        
        total_twitter = data['melbourne']['city_tweet_count'] || 1;
        temp = data['melbourne']['tweet_density'];
        levelA.push(total_twitter / temp['unique_user_count']);
        levelB.push(temp['english_mother_tongue_proportion']);
        
        total_twitter = data['brisbane']['city_tweet_count'] || 1;
        temp = data['brisbane']['tweet_density'];
        levelA.push(total_twitter / temp['unique_user_count']);
        levelB.push(temp['english_mother_tongue_proportion']);
        
        total_twitter = data['sydney']['city_tweet_count'] || 1;
        temp = data['sydney']['tweet_density'];
        levelA.push(total_twitter / temp['unique_user_count']);
        levelB.push(temp['english_mother_tongue_proportion']);

        total_twitter = data['perth']['city_tweet_count'] || 1;
        temp = data['perth']['tweet_density'];
        levelA.push(total_twitter / temp['unique_user_count']);
        levelB.push(temp['english_mother_tongue_proportion']);
        
        this.denData = {
            labels: ['Adelaide', 'Melbourne', 'Brisbane', 'Sydney', 'Perth'],
            datasets: [
                {
                    label: 'Tweets per user',
                    data: levelA,
                    type: 'line',
                    yAxisID: 'y2',
                    borderColor: '#0a1D30',
                    fill: false,
                    
                },
                {
                    label: 'Proportion of people whose mother tongue is English',
                    data: levelB,
                    yAxisID: 'y1',
                    
                }
            ],
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
.footer {
    margin: 20px;
    color: '#486C82';

    h2 {
        margin: 40px;
    }
    h4 {
        margin: 20px;
    }
}
</style>
