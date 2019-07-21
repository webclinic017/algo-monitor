import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Result from './views/Result.vue'
import ResultsList from './views/ResultsList.vue'
import RunStrat from './views/RunStrat.vue'
import Upload from './views/Upload.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/result',
      name: 'result',
      component: Result
    },
    {
      path: '/results-list',
      name: 'results-list',
      component: ResultsList
    },
    {
      path: '/run-strat',
      name: 'run-strat',
      component: RunStrat
    },
    {
      path: '/upload',
      name: 'upload',
      component: Upload
    }
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    // }
  ]
})
