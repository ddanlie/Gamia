import { createRouter, createWebHistory, createWebHashHistory, createMemoryHistory  } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RecycleGameView from '@/views/xdomra00Views/RecycleGameView.vue'
import RiddleGameView from '@/views/xivano08Views/RiddleGameView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: '/',
    //   name: 'home',
    //   component: HomeView
    // },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // }
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/RecycleGame',
      name: 'Recycle',
      component: RecycleGameView
    },
    {
      path: '/RiddleGame',
      name: 'Riddle',
      component: RiddleGameView
    },
  ]
})

export default router
