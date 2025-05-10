// import router from './index'
// import { auth } from '@/api'
// import { ElMessage } from 'element-plus'

// // 路由守卫
// router.beforeEach(async (to, from, next) => {
//   // 获取本地存储的用户Token
//   const token = localStorage.getItem('token')
//   const user = JSON.parse(localStorage.getItem('user') || '{}')
  
//   // 如果前往登录/注册页
//   if (to.path === '/login' || to.path === '/register') {
//     if (token) {
//       // 已登录用户重定向到主页
//       next({ path: '/' })
//     } else {
//       // 未登录用户允许前往登录/注册页
//       next()
//     }
//     return
//   }
  
//   // 检查是否需要认证
//   if (to.meta.requiresAuth !== false) {
//     // 需要认证但没有token
//     if (!token) {
//       ElMessage.error('您需要先登录才能访问该页面')
//       next({ path: '/login', query: { redirect: to.fullPath } })
//       return
//     }
    
//     // 检查路由是否需要特定角色
//     if (to.meta.roles && to.meta.roles.length > 0) {
//       try {
//         // 检查用户是否有权限访问该路由
//         const requiredRole = to.meta.roles[0] // 取第一个所需角色
//         const response = await auth.checkRole(requiredRole)
        
//         if (response.status === 'success' && response.data && response.data.hasRole) {
//           // 有权限，继续
//           next()
//         } else {
//           // 无权限，重定向到403页面
//           ElMessage.error('您没有权限访问该页面')
//           next({ path: '/403' })
//         }
//       } catch (error) {
//         console.error('权限检查失败:', error)
//         ElMessage.error('权限验证失败，请重新登录')
//         localStorage.removeItem('token')
//         localStorage.removeItem('user')
//         next({ path: '/login' })
//       }
//       return
//     }
//   }
  
//   // 其他情况放行
//   next()
// })

// export default router 

// import { auth } from '@/api'
// import { ElMessage } from 'element-plus'

// // 路由守卫逻辑
// export function setupRouterGuard(router) {
//   router.beforeEach(async (to, from, next) => {
//     // 获取本地存储的 token 和 user，添加安全解析
//     const token = localStorage.getItem('token')
//     let user = {}
//     try {
//       user = JSON.parse(localStorage.getItem('user') || '{}')
//     } catch (error) {
//       console.error('解析用户信息失败:', error)
//       localStorage.removeItem('user')
//     }

//     // 如果前往登录/注册页
//     if (to.path === '/login' || to.path === '/register') {
//       if (token) {
//         // 已登录用户重定向到主页
//         next({ path: '/' })
//       } else {
//         // 未登录用户允许前往登录/注册页
//         next()
//       }
//       return
//     }

//     // 检查是否需要认证
//     if (to.meta?.requiresAuth !== false) {
//       // 需要认证但没有 token
//       if (!token) {
//         ElMessage.error('您需要先登录才能访问该页面')
//         next({ path: '/login', query: { redirect: to.fullPath } })
//         return
//       }

//       // 检查路由是否需要特定角色
//       if (to.meta?.roles?.length > 0) {
//         try {
//           const requiredRole = to.meta.roles[0] // 取第一个所需角色
//           const response = await auth.checkRole(requiredRole)

//           if (response.status === 'success' && response.data?.hasRole) {
//             // 有权限，继续
//             next()
//           } else {
//             // 无权限，重定向到 403 页面
//             ElMessage.error('您没有权限访问该页面')
//             next({ path: '/403' })
//           }
//         } catch (error) {
//           console.error('权限检查失败:', error)
//           ElMessage.error('权限验证失败，请重新登录')
//           localStorage.removeItem('token')
//           localStorage.removeItem('user')
//           next({ path: '/login' })
//         }
//         return
//       }
//     }

//     // 其他情况放行
//     next()
//   })
// }
// export default router 

import { auth } from '@/api'
import { ElMessage } from 'element-plus'

// 路由守卫逻辑
export function setupRouterGuard(router) {
  router.beforeEach(async (to, from, next) => {
    // 获取本地存储的 token 和 user，添加安全解析
    const token = localStorage.getItem('token')
    let user = {}
    try {
      user = JSON.parse(localStorage.getItem('user') || '{}')
    } catch (error) {
      console.error('解析用户信息失败:', error)
      localStorage.removeItem('user')
    }

    // 如果前往登录/注册页
    if (to.path === '/login' || to.path === '/register') {
      if (token) {
        // 已登录用户重定向到主页
        next({ path: '/' })
      } else {
        // 未登录用户允许前往登录/注册页
        next()
      }
      return
    }

    // 检查是否需要认证
    if (to.meta?.requiresAuth !== false) {
      // 需要认证但没有 token
      if (!token) {
        ElMessage.error('您需要先登录才能访问该页面')
        next({ path: '/login', query: { redirect: to.fullPath } })
        return
      }

      // 检查路由是否需要特定角色
      if (to.meta?.roles?.length > 0) {
        try {
          const requiredRole = to.meta.roles[0] // 取第一个所需角色
          const response = await auth.checkRole(requiredRole)

          if (response.status === 'success' && response.data?.hasRole) {
            // 有权限，继续
            next()
          } else {
            // 无权限，重定向到 403 页面
            ElMessage.error('您没有权限访问该页面')
            next({ path: '/403' })
          }
        } catch (error) {
          console.error('权限检查失败:', error)
          ElMessage.error('权限验证失败，请重新登录')
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          next({ path: '/login' })
        }
        return
      }
    }

    // 其他情况放行
    next()
  })
}