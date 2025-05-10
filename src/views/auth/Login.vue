<template>
  <div class="login-container">
    <el-card class="login-card">
      <div class="login-header">
        <img src="/src/assets/logo.svg" alt="Logo" class="login-logo" />
        <h2>银行客户画像系统</h2>
      </div>
      <el-form
        ref="loginForm"
        :model="loginData"
        :rules="loginRules"
        label-position="top"
      >
        <el-form-item label="角色" prop="role">
          <el-select v-model="loginData.role" placeholder="请选择登录角色" class="w-100">
            <el-option label="客户" value="customer" />
            <el-option label="客户经理" value="manager" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginData.username"
            placeholder="请输入用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginData.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="loginData.remember">记住我</el-checkbox>
          <el-link type="primary" class="float-right">忘记密码？</el-link>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" class="w-100" :loading="loading" @click="handleLogin">
            登录
          </el-button>
        </el-form-item>
        
        <div class="text-center">
          <span>还没有账号？</span>
          <el-link type="primary" @click="$router.push('/register')">立即注册</el-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { auth } from '@/api'

const router = useRouter()
const loginForm = ref(null)
const loading = ref(false)

const loginData = reactive({
  role: '',
  username: '',
  password: '',
  remember: false
})

const loginRules = {
  role: [{ required: true, message: '请选择登录角色', trigger: 'change' }],
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  if (!loginForm.value) return
  
  try {
    await loginForm.value.validate()
    loading.value = true
    
    // 使用API服务调用登录
    const data = await auth.login(loginData)
    
    localStorage.setItem('token', data.token)
    localStorage.setItem('user', JSON.stringify(data.user))
    
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch (error) {
    console.error('登录失败：', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1f4037 0%, #99f2c8 100%);
  
  .login-card {
    width: 420px;
    padding: 20px;
    
    .login-header {
      text-align: center;
      margin-bottom: 30px;
      
      .login-logo {
        width: 64px;
        height: 64px;
        margin-bottom: 16px;
      }
      
      h2 {
        margin: 0;
        color: #303133;
        font-size: 24px;
      }
    }
  }
}

.w-100 {
  width: 100%;
}

.float-right {
  float: right;
}

.text-center {
  text-align: center;
}
</style>