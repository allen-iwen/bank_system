<template>
  <el-container class="app-container">
    <el-aside width="250px" class="aside">
      <div class="logo">
        <img src="/src/assets/logo.svg" alt="Logo" />
        <span>银行客户画像系统</span>
      </div>
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical"
        router
      >
        <!-- 管理员和客户经理菜单 -->
        <template v-if="userRole === 'admin' || userRole === 'manager'">
          <el-menu-item index="/dashboard">
            <el-icon><DataLine /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          <el-menu-item index="/customers" v-if="userRole === 'admin' || userRole === 'manager'">
            <el-icon><User /></el-icon>
            <span>客户管理</span>
          </el-menu-item>
          <el-menu-item index="/managers" v-if="userRole === 'admin'">
            <el-icon><UserFilled /></el-icon>
            <span>客户经理管理</span>
          </el-menu-item>
          <el-menu-item index="/matching" v-if="userRole === 'admin'">
            <el-icon><Connection /></el-icon>
            <span>智能匹配</span>
          </el-menu-item>
          <el-menu-item index="/reports" v-if="userRole === 'admin' || userRole === 'manager'">
            <el-icon><PieChart /></el-icon>
            <span>统计报表</span>
          </el-menu-item>
        </template>
        
        <!-- 客户菜单 -->
        <template v-if="userRole === 'customer'">
          <el-menu-item index="/customer/profile">
            <el-icon><User /></el-icon>
            <span>个人中心</span>
          </el-menu-item>
          <el-menu-item index="/customer/services">
            <el-icon><Service /></el-icon>
            <span>我的服务</span>
          </el-menu-item>
          <el-menu-item index="/customer/products">
            <el-icon><Goods /></el-icon>
            <span>金融产品</span>
          </el-menu-item>
        </template>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header height="60px" class="header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentRoute }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-profile">
              <el-avatar :size="32" icon="UserFilled" />
              {{ username }}
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleProfile">个人信息</el-dropdown-item>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main>
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { DataLine, User, UserFilled, Connection, PieChart, Service, Goods } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const username = ref('用户')
const userRole = ref('')

// 路由与菜单项文本的映射
const routeMap = computed(() => {
  return {
    // 管理员和经理路由
    '/dashboard': '仪表盘',
    '/customers': '客户管理',
    '/managers': '客户经理管理',
    '/matching': '智能匹配',
    '/reports': '统计报表',
    // 客户路由
    '/customer/profile': '个人中心',
    '/customer/services': '我的服务',
    '/customer/products': '金融产品'
  }
})

const currentRoute = computed(() => {
  return routeMap.value[route.path] || '首页'
})

onMounted(() => {
  // 获取用户信息
  const userData = localStorage.getItem('user')
  if (userData) {
    try {
      const user = JSON.parse(userData)
      username.value = user.username || '用户'
      userRole.value = user.role || 'customer' // 默认为客户角色
    } catch (error) {
      console.error('解析用户数据失败:', error)
      userRole.value = 'customer' // 出错时默认为客户角色
    }
  } else {
    // 未找到用户数据时，可能需要重定向到登录页
    userRole.value = 'customer' // 默认为客户角色
  }
})

const handleProfile = () => {
  // 根据用户角色决定个人信息页面的路由
  if (userRole.value === 'customer') {
    router.push('/customer/profile')
  } else {
    router.push('/profile')
  }
}

const handleLogout = async () => {
  try {
    // 清除本地存储的用户信息
    localStorage.removeItem('user')
    localStorage.removeItem('token')
    await router.push('/login')
  } catch (error) {
    console.error('退出登录失败:', error)
  }
}
</script>

<style scoped lang="scss">
.app-container {
  height: 100vh;
}

.aside {
  background-color: #304156;
  color: #fff;
  
  .logo {
    height: 60px;
    display: flex;
    align-items: center;
    padding: 0 20px;
    
    img {
      width: 32px;
      height: 32px;
      margin-right: 12px;
    }
    
    span {
      font-size: 18px;
      font-weight: 600;
      white-space: nowrap;
    }
  }
  
  .el-menu {
    border-right: none;
    background-color: transparent;
  }
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  
  .header-right {
    .user-profile {
      display: flex;
      align-items: center;
      cursor: pointer;
      
      .el-avatar {
        margin-right: 8px;
      }
    }
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>