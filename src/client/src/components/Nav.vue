<template>
    <header id="header" class="alt">
        <b-button @click="change" class="more" :variant="variant">{{ this.text}} </b-button>
    </header>
</template>

<script>
export default {
    name: 'Nav',
    data() {
        return {
            to: '',
            variant: '',
            text: '',
        }
    },
    mounted() {
        this.to = '#map';
        if(location.hash === '#statistics') {
            this.to = '#statistics';
        } 
        this.change();
    },
    methods: {
        change() {
            if(this.to === '#map') {
                this.toMap();
            } else {
                this.toStatistics();
            }
        },
        toMap() {
            location.href = this.to;
            this.to = '#statistics';
            this.variant = 'primary';
            this.text = 'View Statistics'; 
        },
        toStatistics() {
            location.href = this.to;
            this.to = '#map';
            this.variant = 'outline-primary'
            this.text = 'View Map';
        }
    }

}
</script>

<style scoped lang="less">
@import '~bootstrap/dist/css/bootstrap.css';
@import '~bootstrap-vue/dist/bootstrap-vue.css';
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