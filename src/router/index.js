// import { createRouter, createWebHistory } from 'vue-router'

// const routes = [
//   {
//     path: '/login',
//     name: 'Login',
//     component: () => import('@/views/auth/Login.vue'),
//     meta: { requiresAuth: false }
//   },
//   {
//     path: '/register',
//     name: 'Register',
//     component: () => import('@/views/auth/Register.vue'),
//     meta: { requiresAuth: false }
//   },
//   {
//     path: '/403',
//     name: 'Forbidden',
//     component: () => import('@/views/error/Forbidden.vue'),
//     meta: { requiresAuth: false }
//   },
//   {
//     path: '/',
//     redirect: to => {
//       // 根据用户角色决定重定向的路径
//       const userData = localStorage.getItem('user')
//       if (userData) {
//         try {
//           const user = JSON.parse(userData)
//           if (user.role === 'customer') {
//             return '/customer/profile'
//           }
//         } catch (error) {
//           console.error('解析用户数据失败:', error)
//         }
//       }
//       return '/dashboard'
//     },
//     meta: { requiresAuth: true }
//   },
//   {
//     path: '/dashboard',
//     name: 'Dashboard',
//     component: () => import('@/views/dashboard/Index.vue'),
//     meta: { requiresAuth: true, roles: ['admin', 'manager'] }
//   },
//   {
//     path: '/customers',
//     name: 'Customers',
//     component: () => import('@/views/customers/Index.vue'),
//     meta: { requiresAuth: true, roles: ['admin', 'manager'] }
//   },
//   {
//     path: '/managers',
//     name: 'Managers',
//     component: () => import('@/views/managers/Index.vue'),
//     meta: { requiresAuth: true, roles: ['admin'] }
//   },
//   {
//     path: '/matching',
//     name: 'Matching',
//     component: () => import('@/views/matching/Index.vue'),
//     meta: { requiresAuth: true, roles: ['admin'] }
//   },
//   {
//     path: '/reports',
//     name: 'Reports',
//     component: () => import('@/views/reports/Index.vue'),
//     meta: { requiresAuth: true, roles: ['admin', 'manager'] }
//   },
//   {
//     path: '/profile',
//     name: 'Profile',
//     component: () => import('@/views/profile/Index.vue'),
//     meta: { requiresAuth: true }
//   },
//   // 客户专用页面
//   {
//     path: '/customer/profile',
//     name: 'CustomerProfile',
//     component: () => import('@/views/customer/Profile.vue'),
//     meta: { requiresAuth: true, roles: ['customer'] }
//   },
//   {
//     path: '/customer/services',
//     name: 'CustomerServices',
//     component: () => import('@/views/customer/Services.vue'),
//     meta: { requiresAuth: true, roles: ['customer'] }
//   },
//   {
//     path: '/customer/products',
//     name: 'CustomerProducts',
//     component: () => import('@/views/customer/Products.vue'),
//     meta: { requiresAuth: true, roles: ['customer'] }
//   },
//   // 通配路由必须放在最后
//   {
//     path: '/:pathMatch(.*)*',
//     name: 'NotFound',
//     component: () => import('@/views/error/NotFound.vue'),
//     meta: { requiresAuth: false }
//   }
// ]

// const router = createRouter({
//   history: createWebHistory(),
//   routes
// })

// // 移除旧的路由守卫，使用permission.js中的守卫
// // 导入permission.js将自动应用路由守卫
// import './permission'

// export default router

import { createRouter, createWebHistory } from 'vue-router'
import { setupRouterGuard } from './permission'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/403',
    name: 'Forbidden',
    component: () => import('@/views/error/Forbidden.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: to => {
      // 根据用户角色决定重定向的路径
      const userData = localStorage.getItem('user')
      if (userData) {
        try {
          const user = JSON.parse(userData)
          if (user.role === 'customer') {
            return '/customer/profile'
          }
        } catch (error) {
          console.error('解析用户数据失败:', error)
        }
      }
      return '/dashboard'
    },
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/dashboard/Index.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'manager'] }
  },
  {
    path: '/customers',
    name: 'Customers',
    component: () => import('@/views/customers/Index.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'manager'] }
  },
  {
    path: '/managers',
    name: 'Managers',
    component: () => import('@/views/managers/Index.vue'),
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/matching',
    name: 'Matching',
    component: () => import('@/views/matching/Index.vue'),
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('@/views/reports/Index.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'manager'] }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/profile/Index.vue'),
    meta: { requiresAuth: true }
  },
  // 客户专用页面
  {
    path: '/customer/profile',
    name: 'CustomerProfile',
    component: () => import('@/views/customer/Profile.vue'),
    meta: { requiresAuth: true, roles: ['customer'] }
  },
  {
    path: '/customer/services',
    name: 'CustomerServices',
    component: () => import('@/views/customer/Services.vue'),
    meta: { requiresAuth: true, roles: ['customer'] }
  },
  {
    path: '/customer/products',
    name: 'CustomerProducts',
    component: () => import('@/views/customer/Products.vue'),
    meta: { requiresAuth: true, roles: ['customer'] }
  },
  // 通配路由必须放在最后
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/NotFound.vue'),
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 应用路由守卫
setupRouterGuard(router)

export default router
