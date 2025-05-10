<template>
  <div class="forbidden-container">
    <div class="forbidden-content">
      <h1>403</h1>
      <h2>禁止访问</h2>
      <p>抱歉，您没有权限访问该页面</p>
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
.forbidden-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f8f9fa;
}

.forbidden-content {
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
  color: #f56c6c;
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