import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import ResultId from './views/ResultId.vue'
import ResultLabel from './views/ResultLabel.vue'
import ResultsList from './views/ResultsList.vue'
import StratRun from './views/StratRun.vue'
import StratCreate from './views/StratCreate.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      meta: {
        title: 'Home'
      },
      component: Home
    },
    {
      path: '/result/id/:id',
      name: 'result-id',
      meta: {
        title: 'Resultado'
      },
      component: ResultId
    },
    {
      path: '/result/label/:label',
      name: 'result-label',
      meta: {
        title: 'Resultado'
      },
      component: ResultLabel
    },
    {
      path: '/results',
      name: 'results',
      meta: {
        title: 'Resultados'
      },
      component: ResultsList
    },
    {
      path: '/strat/run',
      name: 'strat-run',
      meta: {
        title: 'Rodar Estratégia'
      },
      component: StratRun
    },
    {
      path: '/strat/create',
      name: 'strat-create',
      meta: {
        title: 'Criar Estratégia'
      },
      component: StratCreate
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
