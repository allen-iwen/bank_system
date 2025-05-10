<template>
  <div class="register-container">
    <el-card class="register-card">
      <div class="register-header">
        <img src="/src/assets/logo.svg" alt="Logo" class="register-logo" />
        <h2>银行客户画像系统</h2>
      </div>
      <el-form
        ref="registerForm"
        :model="registerData"
        :rules="registerRules"
        label-position="top"
      >
        <el-form-item label="角色" prop="role">
          <el-select v-model="registerData.role" placeholder="请选择注册角色" class="w-100">
            <el-option label="客户" value="customer" />
            <el-option label="客户经理" value="manager" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerData.username"
            placeholder="请输入用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="registerData.email"
            placeholder="请输入邮箱"
            prefix-icon="Message"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerData.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerData.confirmPassword"
            type="password"
            placeholder="请确认密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="姓名" prop="name">
          <el-input
            v-model="registerData.name"
            placeholder="请输入姓名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <template v-if="registerData.role === 'customer'">
          <el-form-item label="年龄" prop="age">
            <el-input-number
              v-model="registerData.age"
              :min="18"
              :max="100"
              class="w-100"
            />
          </el-form-item>
          
          <el-form-item label="职业" prop="occupation">
            <el-input
              v-model="registerData.occupation"
              placeholder="请输入职业"
            />
          </el-form-item>
          
          <el-form-item label="总资产（万元）" prop="totalAssets">
            <el-input-number
              v-model="registerData.totalAssets"
              :min="0"
              :precision="2"
              :step="10"
              class="w-100"
            />
          </el-form-item>
        </template>
        
        <template v-if="registerData.role === 'manager'">
          <el-form-item label="专业能力" prop="capabilities">
            <el-select
              v-model="registerData.capabilities"
              multiple
              filterable
              allow-create
              placeholder="请选择或输入专业能力"
              class="w-100"
            >
              <el-option
                v-for="item in capabilityOptions"
                :key="item"
                :label="item"
                :value="item"
              />
            </el-select>
          </el-form-item>
        </template>
        
        <el-form-item label="兴趣爱好" prop="hobbies">
          <el-select
            v-model="registerData.hobbies"
            multiple
            filterable
            allow-create
            placeholder="请选择或输入兴趣爱好"
            class="w-100"
          >
            <el-option
              v-for="item in hobbyOptions"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" class="w-100" :loading="loading" @click="handleRegister">
            注册
          </el-button>
        </el-form-item>
        
        <div class="text-center">
          <span>已有账号？</span>
          <el-link type="primary" @click="$router.push('/login')">立即登录</el-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue'

const router = useRouter()
const registerForm = ref(null)
const loading = ref(false)

const capabilityOptions = [
  '理财规划',
  '投资咨询',
  '风险管理',
  '保险规划',
  '税务筹划',
  '资产配置'
]

const hobbyOptions = [
  '阅读',
  '旅游',
  '运动',
  '音乐',
  '摄影',
  '书法',
  '绘画'
]

const registerData = reactive({
  role: '',
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  name: '',
  age: 18,
  occupation: '',
  totalAssets: 0,
  capabilities: [],
  hobbies: []
})

const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else {
    if (registerData.confirmPassword !== '') {
      registerForm.value.validateField('confirmPassword')
    }
    callback()
  }
}

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerData.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const registerRules = {
  role: [{ required: true, message: '请选择注册角色', trigger: 'change' }],
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [{ validator: validatePass, trigger: 'blur' }],
  confirmPassword: [{ validator: validatePass2, trigger: 'blur' }],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
  occupation: [{ required: true, message: '请输入职业', trigger: 'blur' }],
  totalAssets: [{ required: true, message: '请输入总资产', trigger: 'blur' }],
  capabilities: [{ required: true, message: '请选择专业能力', trigger: 'change' }],
  hobbies: [{ required: true, message: '请选择兴趣爱好', trigger: 'change' }]
}

const handleRegister = async () => {
  if (!registerForm.value) return
  
  try {
    await registerForm.value.validate()
    loading.value = true
    
    // 调用注册API
    const response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(registerData)
    })
    
    const data = await response.json()
    
    if (response.ok) {
      ElMessage.success('注册成功')
      router.push('/login')
    } else {
      ElMessage.error(data.message || '注册失败')
    }
  } catch (error) {
    ElMessage.error('注册失败：' + error.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1f4037 0%, #99f2c8 100%);
  padding: 20px 0;
  
  .register-card {
    width: 420px;
    
    .register-header {
      text-align: center;
      margin-bottom: 30px;
      
      .register-logo {
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

.text-center {
  text-align: center;
}
</style>