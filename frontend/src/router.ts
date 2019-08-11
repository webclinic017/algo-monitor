import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import ResultId from './views/ResultId.vue'
import ResultLabel from './views/ResultLabel.vue'
import ResultsList from './views/ResultsList.vue'
import StratRun from './views/StratRun.vue'
import StratCreate from './views/StratCreate.vue'
import ProcessStatus from './views/ProcessStatus.vue'
import StratList from './views/StratList.vue'
import NotFound from './views/NotFound.vue'

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
      path: '/process',
      name: 'process',
      meta: {
        title: 'Processos'
      },
      component: ProcessStatus
    },
    {
      path: '/strat/run',
      name: 'strat-run',
      meta: {
        title: 'Executar Estratégia'
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
    },
    {
      path: '/strat/list',
      name: 'strat-list',
      meta: {
        title: 'Listar Estratégias'
      },
      component: StratList
    },
    { path: '/404', component: NotFound },
    { path: '*', redirect: '/404' },
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
