<template>
    <div class="map">
        <div id="mapCanvas" style="height: 100vh; width: 100%"></div>
        <div class="map__select-area">
            <b-form-select v-model="city" :options="cityOptions" :style="{margin: '2px 0'}"></b-form-select>
            <b-form-select v-model="type" :options="typeOptions" :style="{margin: '2px 0'}"></b-form-select>
            <b-card title="Tips" style="text-align: left;margin: '2px 0'" v-if="tips">
                {{ tips }}
            </b-card>
        </div>
    </div>
</template>

<script>
import { mapStyle } from '../assets/mapStyle';
import { mock } from '../assets/mock.js';
import { BFormSelect, BCard  } from 'bootstrap-vue';
import Prompt from './Prompt';
import Vue from 'vue';
//  const vicMap = 'https://data.gov.au/geoserver/vic-local-government-areas-psma-administrative-boundaries/wfs?request=GetFeature&typeName=ckan_bdf92691_c6fe_42b9_a0e2_a4cd716fa811&outputFormat=json';
//  const melbMap = 'https://raw.githubusercontent.com/HanxunHuangLemonBear/COMP90024-2019S1-Team7-TrackerHub/master/backend/backend/common/melb_geo.json'
import { ROOT } from '../utils/Api';
const melbourneMap = ROOT + 'api/statistic?city=melbourne';
const perthMap = ROOT + 'api/statistic?city=perth';
const adelaideMap = ROOT + 'api/statistic?city=adelaide';
const sydneyMap = ROOT + 'api/statistic?city=sydney';
const brisbaneMap = ROOT + 'api/statistic?city=brisbane';

const { aurin } = mock;

export default {
    name: 'map',
    components: {
        'b-form-select': BFormSelect,
        'prompt': Prompt,
        'b-card': BCard,
    },
    data() {
        return {
            map: null,
            aurinMap: null,
            city: null,
            type: null,
            cityOptions: [
                { value: null, text: 'Please select a city', disabled: true},
                { value: 'Melbourne', text: 'Melbourne'},
                { value: 'Sydney', text: 'Sydney'},
                { value: 'Adelaide', text: 'Adelaide'},
                { value: 'Perth', text: 'Perth'},
                { value: 'Brisbane', text: 'Brisbane'},
            ],
            typeOptions: [
                {value: null, text: 'Please select a scenario', disabled: true},
                {value: 'income', text: 'Scenario1 -- Income level and Tweet sentiment'},
                {value: 'education', text: 'Scenario2 -- Vulgar Tweets and Education'},
                {value: 'migration', text: 'Scenario3 -- Tweeting language and Migration'},
            ],
            //  bar chart
            labelA: '',
            labelB: '',
            theme: '#00FF00',
            barLabel: [],
            barDataA: [],
            barDataB: [],
            tips: '',
        }
    },
    mounted() {
        this.init();
    },
    computed: {
        barChartData() {
            let { barLabel, labelB, labelA, theme, barDataA, barDataB } = this;
            let yID = 'y1';
            if(this.type == 'income') {
                yID = 'y2';
            }
            let temp = {
                labels: barLabel,
                datasets: [
                    {
                        yAxisID: 'y1',
                        label: labelA,
                        backgroundColor: theme,
                        data: barDataA
                    },
                    {
                        yAxisID: yID,
                        label: labelB,
                        backgroundColor: this.gradient('#F1F0E9', this.theme, 7)[2],
                        data: barDataB
                    }
                ]
            }
            return temp;
        }
    },
    watch: {
        city: {
            handler: function(val, oldval) {
                this.changeCity(val);
            },
        },
        type: {
            handler: function(val, oldval) {
                switch(val) {
                    case 'income':
                        this.tips = 'The color shown on the map represents the income level of that region'; 
                        break;
                    case 'education':
                        this.tips = 'The color shown on the map represents the frequency of vulgar expression occurence';
                        break;
                    case 'migration':
                        this.tips = 'The color shown on the map represents the ratio of non-english twitter';
                        break;
                    default:
                        this.tips = '';
                }
                this.mapAurin(this.aurinMap, val);
            },
        },
        barChartData: {
            handler: function(val, oldval) {
                this.$emit('setBarChartData', val);
            },
        }
    },
    methods: {
        changeCity(city) {
            switch(city) {
                case 'Melbourne': 
                    this.toMelbourne();
                    break;
                case 'Sydney':
                    this.toSydney();
                    break;
                case 'Adelaide':
                    this.toAdelaide();
                    break;
                case 'Perth':
                    this.toPerth();
                    break;
                case 'Brisbane':
                    this.toBrisbane();
                    break;
            }
        },
        toMelbourne() {
            this.map = new google.maps.Map(document.getElementById('mapCanvas'), {
                zoom: 11.8,
                center:  {lat: -37.7998, lng: 144.90},
                disableDefaultUI: true,
                styles: mapStyle,
            });
            this.aurinMap = melbourneMap;
            this.mapAurin(melbourneMap, this.type);
        },
        toSydney() {
            this.map = new google.maps.Map(document.getElementById('mapCanvas'), {
                zoom: 11.8,
                center:  {lat: -33.92, lng: 151.1},
                disableDefaultUI: true,
                styles: mapStyle,
            });
            this.aurinMap = sydneyMap;
            this.mapAurin(sydneyMap, this.type);
        },
        toAdelaide() {
            this.map = new google.maps.Map(document.getElementById('mapCanvas'), {
                zoom: 10.5,
                center:  {lat: -34.9, lng: 138.330},
                disableDefaultUI: true,
                styles: mapStyle,
            });
            this.aurinMap = adelaideMap;
            this.mapAurin(adelaideMap, this.type);
        },
        toPerth() {
            this.map = new google.maps.Map(document.getElementById('mapCanvas'), {
                zoom: 11.8,
                center:  {lat: -31.95, lng: 115.72},
                disableDefaultUI: true,
                styles: mapStyle,
            });
            this.aurinMap = perthMap;
            this.mapAurin(perthMap, this.type);
        },
        toBrisbane() {
            this.map = new google.maps.Map(document.getElementById('mapCanvas'), {
                zoom: 11,
                center:  {lat: -27.39, lng: 153},
                disableDefaultUI: true,
                styles: mapStyle,
            });
            this.aurinMap = brisbaneMap;
            this.mapAurin(brisbaneMap, this.type);
        },
        init() {
            this.map = new google.maps.Map(document.getElementById('mapCanvas'), {
                zoom: 4.8,
                center:  {lat: -28, lng: 130},
                disableDefaultUI: true,
                styles: mapStyle,
            });
        },
        gradient (startColor, endColor, step) {
            var sColor = this.hexToRgb(startColor),
                eColor = this.hexToRgb(endColor);

            var rStep = (eColor[0] - sColor[0]) / step,
                gStep = (eColor[1] - sColor[1]) / step,
                bStep = (eColor[2] - sColor[2]) / step;

            var gradientColorArr = [];
            for(var i=0; i < step; i++){
                gradientColorArr.push(this.rgbToHex(parseInt(rStep*i+sColor[0]),parseInt(gStep*i+sColor[1]),parseInt(bStep*i+sColor[2])));
            }
            return gradientColorArr;
        },
        hexToRgb(hex) {
            var rgb = [];
            for(var i=1; i<7; i+=2){
                rgb.push(parseInt("0x" + hex.slice(i,i+2)));
            }
            return rgb;
        },
        rgbToHex(r, g, b) {
            var hex = ((r<<16) | (g<<8) | b).toString(16);
            return "#" + new Array(Math.abs(hex.length-7)).join("0") + hex;
        },
        mapAurin(cityMap, type) {
            let map = this.map;
            let colors;
            map.data.loadGeoJson(cityMap);
            this.barDataA = [];
            this.barDataB = [];
            this.barLabel = [];
            let basic = '#F1F0E9';
            map.data.setStyle((feature) => {
                let result = feature.getProperty('analysis_result');
                let name = feature.getProperty('name');
                
                let color = basic;
             
                switch(type) {
                    case 'education': 
                        this.$emit('setAx', false);
                        this.theme = '#00FF00';
                        colors = this.gradient(basic, this.theme, 7);
                        let { education } = result;
                        var { vulgar_tweet_count, complete_yr_12_proportion = 0 } = education || {};
                        var { suburb_tweet_count } = result;
                        
                        this.labelB = 'Proportion of people with low education achievements';
                        this.labelA = 'Scaled proportion of vulgar tweets';
                        var total;
                        if(!suburb_tweet_count || !vulgar_tweet_count) total = 0;
                        else total = vulgar_tweet_count / suburb_tweet_count * 100;
                        if(!total) total = 0;
                        if(!this.barLabel.includes(name) && complete_yr_12_proportion && total) {
                            this.barDataB.push(100 - complete_yr_12_proportion);
                            this.barLabel.push(name);
                            this.barDataA.push(total * 10);
                        }
                        
                        if (total == 0)
                            color = colors[0]
                        if (total > 0.5)
                            color = colors[1]
                        if (total > 1)
                            color = colors[2]
                        if (total > 2)
                            color = colors[3]
                        if (total > 5)
                            color = colors[4]
                        if (total > 10)
                            color = colors[5]
                        if (total > 20)
                            color = colors[6]  
                        break;
                    case 'income':
                        this.$emit('setAx', true);
                        this.theme = '#007BFF';
                        colors = this.gradient(basic, this.theme, 7);
                        let { income } = result;
                        var { high_income_proportion: total } = income || {};
                        let { 
                            tweet_negative_count = 1,
                            tweet_neutral_count = 1,
                            tweet_positive_count = 1,
                        } = income || {};
                        let ratio;
                        if(!tweet_negative_count)  tweet_negative_count = 1;
                        ratio = tweet_positive_count / tweet_negative_count; 
                       
                        if(!total) total = 0;
                        this.labelB = 'The ratio of #positive tweets to #negative tweets';  
                        this.labelA = 'The proportion of high income people';
                        if(!this.barLabel.includes(name) && total && ratio) {
                            this.barDataA.push(total);
                            this.barLabel.push(name);
                            this.barDataB.push(ratio);
                        }
                        if (total >= 0)
                            color = colors[0]
                        if (total >= 0)
                            color = colors[1]
                        if (total >= 1)
                            color = colors[2]
                        if (total > 10)
                            color = colors[3]
                        if (total > 15)
                            color = colors[4]
                        if (total > 20)
                            color = colors[5]
                        if (total > 30)
                            color = colors[6]
                        break;
                    case 'migration':
                        this.$emit('setAx', false);
                        this.theme = '#FF9900'
                        colors = this.gradient(basic, this.theme, 7);
                        let { migration } = result;
                        var { non_english_tweet_count = 0, not_english_at_home = 0 } = migration || {};
                        var { suburb_tweet_count = 0} = result;
                        var total;
                        if(!non_english_tweet_count || !suburb_tweet_count) total = 0;
                        else total = non_english_tweet_count / suburb_tweet_count * 100;
                        if(!total) total = 0;
                        
                        this.labelA = 'The proportion of non-engligh tweets';  
                        this.labelB = 'The proportion of people don\'t speak Engligh at home';
                        if(!this.barLabel.includes(name) && total && not_english_at_home) {
                            this.barDataA.push(total);
                            this.barLabel.push(name);
                            this.barDataB.push(not_english_at_home);
                        }  
                        if (total >= 0.5)
                            color = colors[0]
                        if (total > 1)
                            color = colors[1]
                        if (total > 2)
                            color = colors[2]
                        if (total > 5)
                            color = colors[3]
                        if (total > 10)
                            color = colors[4]
                        if (total > 20)
                            color = colors[5]
                        if (total > 30)
                            color = colors[6]  
                        break;
                    default:
                        break;
                }
                return {
                    fillColor: color,
                    fillOpacity: 0.7,
                    strokeWeight: 1
                }
            });
            
            let infowindow = new google.maps.InfoWindow();

            map.data.addListener('click', (event) => {
                
                const { feature } = event;
                let result = feature.getProperty('analysis_result');
                const suburb = feature.getProperty('name');
                let name = [];
                let data = [];
         
                switch(type) {
                    case 'income':
                        let { income } = result;
                        let { 
                            tweet_negative_count = 1,
                            tweet_neutral_count = 1,
                            tweet_positive_count = 1,
                            high_income_proportion = 33.3,
                            low_income_proportion = 33.3,
                        } = income || {};
                        let totalTweet = ( tweet_negative_count + tweet_neutral_count + tweet_positive_count ) || 1;
                        name = [ 
                            'attitude of twitter',
                            'income level'
                        ]
                        data = [
                            {
                                labels: ['tweet_negative', 'tweet_neutral', 'tweet_positive'],
                                datasets: [
                                    {
                                        label: 'attitude of twitter',
                                        backgroundColor: this.gradient(basic, this.theme, 3) ,
                                        data: [tweet_negative_count / totalTweet * 100, tweet_neutral_count / totalTweet * 100, tweet_positive_count / totalTweet * 100],
                                    }
                                ]
                            },
                            {
                                labels: ['low_income', 'middle_income', 'high_income'],
                                datasets: [
                                    {
                                        label: 'income level',
                                        backgroundColor: this.gradient(basic, this.theme, 3) ,
                                        data: [low_income_proportion, 100 - low_income_proportion - high_income_proportion, high_income_proportion],
                                    }
                                ]
                            }
                        ];
                        break;
                    case 'education':
                        let { education } = result;
                        var { complete_yr_12_proportion = 0, youth_in_study_or_work_proportion = 0 } = education || {};
                        name = [
                            'education level',
                            'good young man',
                        ]
                        data = [
                            {
                                labels: ['not complete 12 years education', 'complete 12 years education'],
                                datasets: [
                                    {
                                        label: 'education level',
                                        backgroundColor: this.gradient(basic, this.theme, 2),
                                        data: [100 - complete_yr_12_proportion, complete_yr_12_proportion],
                                    }
                                ]
                            },
                            {
                                labels: ['the youngth who are not in study or work', 'the youngth who are in study or work'],
                                datasets: [
                                    {
                                        label: 'good young man',
                                        backgroundColor: this.gradient(basic, this.theme, 2) ,
                                        data: [100 - youth_in_study_or_work_proportion, youth_in_study_or_work_proportion],
                                    }
                                ]
                            }
                        ];
                
                        break;
                    case 'migration':
                        let { migration } = result;
                        var { not_english_at_home = 0, born_overseas_proportion = 0 } = migration || {};
                        name = [
                            'speak language',
                            'born place',
                        ]
                        data = [
                            {
                                labels: ['People don\'t speak English at home', 'People speak English at home'],
                                datasets: [
                                    {
                                        label: 'speak language',
                                        backgroundColor: this.gradient(this.theme, basic, 2) ,
                                        data: [not_english_at_home, 100 - not_english_at_home],
                                    }
                                ]
                            },
                            {
                                labels: ['people born overseas', 'people born in Australia'],
                                datasets: [
                                    {
                                        label: 'born place',
                                        backgroundColor: this.gradient(this.theme, basic, 2) ,
                                        data: [born_overseas_proportion, 100 - born_overseas_proportion],
                                    }
                                ]
                            }
                        ]
                        break;
                    default:
                        break;
                }
                let MyPrompt = Vue.extend(Prompt);
               
                let instance = new MyPrompt({
                    propsData: {
                        name,
                        data,
                        suburb,
                    }
                });
                instance.$mount()
                infowindow.setContent(instance.$el)
        
                infowindow.setPosition(event.latLng);
        
                infowindow.open(map);
            });

            map.data.addListener('mouseover', (event) => {
                map.data.overrideStyle(event.feature, {fillColor: 'rgba(0,0,0,0.5)'});
            })

            map.data.addListener('mouseout', (event) => {
                map.data.revertStyle();
                infowindow.close();
            })
 
        },
    }
}
</script>

<style scoped>
.map {
    position: relative;
}
.map__select-area {
    position: absolute;
    top: 30px;
    left: 30px;
}
</style>
