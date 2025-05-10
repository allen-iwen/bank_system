<template>
  <div class="customers-container">
    <!-- 搜索和过滤区域 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="客户分类">
          <el-select v-model="filterForm.classification" placeholder="选择分类" clearable>
            <el-option v-for="item in classifications" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="资产范围">
          <el-select v-model="filterForm.assetRange" placeholder="选择范围" clearable>
            <el-option label="100万以下" value="0-100" />
            <el-option label="100-500万" value="100-500" />
            <el-option label="500-1000万" value="500-1000" />
            <el-option label="1000万以上" value="1000+" />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input v-model="filterForm.keyword" placeholder="搜索客户姓名/职业" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 客户列表 -->
    <el-card class="list-card">
      <template #header>
        <div class="card-header">
          <span>客户列表</span>
          <el-button type="primary" @click="handleAdd">添加客户</el-button>
        </div>
      </template>
      
      <el-table :data="customerList" style="width: 100%" v-loading="loading">
        <el-table-column type="expand">
          <template #default="props">
            <div class="expand-detail">
              <el-descriptions :column="3" border>
                <el-descriptions-item label="需求列表">
                  <el-tag v-for="demand in props.row.demands" :key="demand" size="small" class="mx-1">
                    {{ demand }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="兴趣爱好">
                  <el-tag v-for="hobby in props.row.hobbies" :key="hobby" size="small" type="success" class="mx-1">
                    {{ hobby }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="创建时间">
                  {{ formatDate(props.row.created_at) }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="age" label="年龄" width="80" />
        <el-table-column prop="occupation" label="职业" width="120" />
        <el-table-column prop="total_assets" label="总资产" width="120">
          <template #default="{ row }">
            {{ formatAssets(row.total_assets) }}
          </template>
        </el-table-column>
        <el-table-column prop="classification" label="客户分类" width="100">
          <template #default="{ row }">
            <el-tag :type="getClassificationTagType(row.classification)">
              {{ row.classification }}类
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="manager" label="客户经理" width="120">
          <template #default="{ row }">
            <el-tag type="info" v-if="row.manager">
              {{ row.manager.name }}
            </el-tag>
            <el-tag type="danger" v-else>未分配</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="150">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="primary" @click="handleAssign(row)">分配</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 客户表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加客户' : '编辑客户'"
      width="50%"
    >
      <el-form
        ref="customerFormRef"
        :model="customerForm"
        :rules="customerRules"
        label-width="100px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="customerForm.name" />
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input-number v-model="customerForm.age" :min="18" :max="100" />
        </el-form-item>
        <el-form-item label="职业" prop="occupation">
          <el-input v-model="customerForm.occupation" />
        </el-form-item>
        <el-form-item label="总资产" prop="total_assets">
          <el-input-number
            v-model="customerForm.total_assets"
            :min="0"
            :precision="2"
            :step="10"
          />
        </el-form-item>
        <el-form-item label="需求" prop="demands">
          <el-select
            v-model="customerForm.demands"
            multiple
            filterable
            allow-create
            placeholder="请选择或输入客户需求"
          >
            <el-option
              v-for="item in demandOptions"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="兴趣爱好" prop="hobbies">
          <el-select
            v-model="customerForm.hobbies"
            multiple
            filterable
            allow-create
            placeholder="请选择或输入兴趣爱好"
          >
            <el-option
              v-for="item in hobbyOptions"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 分配客户经理对话框 -->
    <el-dialog v-model="assignDialogVisible" title="分配客户经理" width="40%">
      <el-form :model="assignForm" label-width="100px">
        <el-form-item label="客户经理">
          <el-select v-model="assignForm.managerId" placeholder="请选择客户经理">
            <el-option
              v-for="manager in managerList"
              :key="manager.id"
              :label="manager.name"
              :value="manager.id"
            >
              <div class="manager-option">
                <span>{{ manager.name }}</span>
                <small class="manager-info">
                  客户数：{{ manager.customerCount }} | 匹配度：{{ manager.matchScore }}%
                </small>
              </div>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="assignDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAssign">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 客户分类选项
const classifications = [
  { label: 'A类', value: 'A' },
  { label: 'B类', value: 'B' },
  { label: 'C类', value: 'C' },
  { label: 'D类', value: 'D' },
  { label: 'E类', value: 'E' }
]

// 需求和爱好选项
const demandOptions = [
  '理财产品',
  '贷款融资',
  '投资咨询',
  '保险规划',
  '财富管理',
  '支付结算'
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

// 过滤表单
const filterForm = reactive({
  classification: '',
  assetRange: '',
  keyword: ''
})

// 客户表单
const customerForm = reactive({
  name: '',
  age: 18,
  occupation: '',
  total_assets: 0,
  demands: [],
  hobbies: []
})

// 分配表单
const assignForm = reactive({
  managerId: ''
})

// 表单校验规则
const customerRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
  occupation: [{ required: true, message: '请输入职业', trigger: 'blur' }],
  total_assets: [{ required: true, message: '请输入总资产', trigger: 'blur' }],
  demands: [{ required: true, message: '请选择需求', trigger: 'change' }],
  hobbies: [{ required: true, message: '请选择兴趣爱好', trigger: 'change' }]
}

// 状态变量
const loading = ref(false)
const dialogVisible = ref(false)
const assignDialogVisible = ref(false)
const dialogType = ref('add')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const customerList = ref([])
const managerList = ref([])
const customerFormRef = ref(null)
const currentCustomer = ref(null)

// 获取客户列表
const fetchCustomers = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/customers', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    const data = await response.json()
    customerList.value = data.customers
    total.value = data.total
  } catch (error) {
    ElMessage.error('获取客户列表失败：' + error.message)
  } finally {
    loading.value = false
  }
}

// 获取客户经理列表
const fetchManagers = async () => {
  try {
    const response = await fetch('/api/managers', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    const data = await response.json()
    managerList.value = data.managers
  } catch (error) {
    ElMessage.error('获取客户经理列表失败：' + error.message)
  }
}

// 格式化资产显示
const formatAssets = (value) => {
  return `${value.toFixed(2)}万元`
}

// 格式化日期
const formatDate = (date) => {
  return new Date(date).toLocaleString()
}

// 获取客户分类标签类型
const getClassificationTagType = (classification) => {
  const typeMap = {
    'A': 'success',
    'B': '',
    'C': 'warning',
    'D': 'danger',
    'E': 'info'
  }
  return typeMap[classification] || 'info'
}

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchCustomers()
}

// 重置表单
const resetForm = () => {
  filterForm.classification = ''
  filterForm.assetRange = ''
  filterForm.keyword = ''
  handleSearch()
}

// 处理分页
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchCustomers()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchCustomers()
}

// 处理添加客户
const handleAdd = () => {
  dialogType.value = 'add'
  Object.keys(customerForm).forEach(key => {
    if (key === 'age') {
      customerForm[key] = 18
    } else if (key === 'total_assets') {
      customerForm[key] = 0
    } else if (Array.isArray(customerForm[key])) {
      customerForm[key] = []
    } else {
      customerForm[key] = ''
    }
  })
  dialogVisible.value = true
}

// 处理编辑客户
const handleEdit = (row) => {
  dialogType.value = 'edit'
  Object.keys(customerForm).forEach(key => {
    customerForm[key] = row[key]
  })
  dialogVisible.value = true
}

// 处理删除客户
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除该客户吗？', '提示', {
      type: 'warning'
    })
    
    const response = await fetch(`/api/customers/${row.id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    if (response.ok) {
      ElMessage.success('删除成功')
      fetchCustomers()
    } else {
      const data = await response.json()
      ElMessage.error(data.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败：' + error.message)
    }
  }
}

// 处理分配客户经理
const handleAssign = (row) => {
  currentCustomer.value = row
  assignForm.managerId = row.manager ? row.manager.id : ''
  assignDialogVisible.value = true
}

// 提交表单
const submitForm = async () => {
  if (!customerFormRef.value) return
  
  try {
    await customerFormRef.value.validate()
    const method = dialogType.value === 'add' ? 'POST' : 'PUT'
    const url = dialogType.value === 'add' ? '/api/customers' : `/api/customers/${customerForm.id}`
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(customerForm)
    })
    
    if (response.ok) {
      ElMessage.success(dialogType.value === 'add' ? '添加成功' : '更新成功')
      dialogVisible.value = false
      fetchCustomers()
    } else {
      const data = await response.json()
      ElMessage.error(data.message || (dialogType.value === 'add' ? '添加失败' : '更新失败'))
    }
  } catch (error) {
    ElMessage.error((dialogType.value === 'add' ? '添加' : '更新') + '失败：' + error.message)
  }
}

// 提交分配
const submitAssign = async () => {
  try {
    const response = await fetch(`/api/customers/${currentCustomer.value.id}/assign`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        manager_id: assignForm.managerId
      })
    })
    
    if (response.ok) {
      ElMessage.success('分配成功')
      assignDialogVisible.value = false
      fetchCustomers()
    } else {
      const data = await response.json()
      ElMessage.error(data.message || '分配失败')
    }
  } catch (error) {
    ElMessage.error('分配失败：' + error.message)
  }
}

// 初始化
onMounted(() => {
  fetchCustomers()
  fetchManagers()
})
</script>

<style scoped lang="scss">
.customers-container {
  padding: 20px;
  
  .filter-card {
    margin-bottom: 20px;
  }
  
  .list-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
  
  .expand-detail {
    padding: 20px;
    
    .el-tag {
      margin-right: 8px;
      margin-bottom: 8px;
    }
  }
  
  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
  
  .manager-option {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .manager-info {
      color: #909399;
    }
  }
}
</style>