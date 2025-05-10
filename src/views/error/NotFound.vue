<template>
  <div class="notfound-container">
    <div class="notfound-content">
      <h1>404</h1>
      <h2>页面未找到</h2>
      <p>抱歉，您请求的页面不存在</p>
      <el-button type="primary" @click="goBack">返回上一页</el-button>
      <el-button @click="goHome">返回首页</el-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.go(-1)
}

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.notfound-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f8f9fa;
}

.notfound-content {
  text-align: center;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 500px;
}

h1 {
  font-size: 6rem;
  margin: 0;
  color: #409eff;
}

h2 {
  font-size: 2rem;
  margin: 0.5rem 0 1.5rem;
  color: #303133;
}

p {
  margin-bottom: 2rem;
  color: #606266;
  font-size: 1.1rem;
}
</style> 