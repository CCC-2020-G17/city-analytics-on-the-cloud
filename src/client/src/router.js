import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

const Home = () => import('./views/Home');
const Front = () => import('./views/Front');
export default new Router({
  routes: [
    {
      path: '/',
      component: Front,
    },
    {
      path: '/map',
      component: Home,
    }
  ],
	mode: 'history',
});