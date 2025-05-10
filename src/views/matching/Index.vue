<template>
  <div class="matching-container">
    <!-- 匹配控制面板 -->
    <el-card class="control-card">
      <el-form :inline="true" :model="matchingForm">
        <el-form-item label="匹配模式">
          <el-radio-group v-model="matchingForm.mode">
            <el-radio-button label="auto">自动匹配</el-radio-button>
            <el-radio-button label="manual">手动调整</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="匹配范围">
          <el-select v-model="matchingForm.scope" placeholder="选择匹配范围">
            <el-option label="全部客户" value="all" />
            <el-option label="未分配客户" value="unassigned" />
            <el-option label="待重新分配" value="reassign" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="matching" @click="startMatching">
            开始匹配
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 匹配结果展示 -->
    <el-card class="result-card">
      <template #header>
        <div class="card-header">
          <span>匹配结果</span>
          <div class="header-actions">
            <el-button type="success" :disabled="!hasMatchResults" @click="applyMatching">
              应用匹配结果
            </el-button>
            <el-button type="info" :disabled="!hasMatchResults" @click="exportMatching">
              导出结果
            </el-button>
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="matchingResults"
        style="width: 100%"
      >
        <el-table-column type="expand">
          <template #default="props">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="匹配原因">
                {{ props.row.matchReason }}
              </el-descriptions-item>
              <el-descriptions-item label="共同兴趣">
                <el-tag
                  v-for="interest in props.row.commonInterests"
                  :key="interest"
                  size="small"
                  class="mx-1"
                >
                  {{ interest }}
                </el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </template>
        </el-table-column>

        <el-table-column label="客户信息">
          <template #default="{ row }">
            <div class="info-cell">
              <span class="name">{{ row.customer.name }}</span>
              <el-tag size="small" :type="getClassificationTagType(row.customer.classification)">
                {{ row.customer.classification }}类
              </el-tag>
              <span class="detail">
                {{ row.customer.age }}岁 | {{ row.customer.occupation }} | 
                资产: {{ formatAssets(row.customer.total_assets) }}
              </span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="客户经理">
          <template #default="{ row }">
            <div class="info-cell">
              <template v-if="matchingForm.mode === 'manual'">
                <el-select v-model="row.manager.id" class="manager-select">
                  <el-option
                    v-for="manager in availableManagers"
                    :key="manager.id"
                    :label="manager.name"
                    :value="manager.id"
                  >
                    <div class="manager-option">
                      <span>{{ manager.name }}</span>
                      <small>当前客户数：{{ manager.customerCount }}</small>
                    </div>
                  </el-option>
                </el-select>
              </template>
              <template v-else>
                <span class="name">{{ row.manager.name }}</span>
                <span class="detail">
                  客户数：{{ row.manager.customerCount }} | 
                  专长：{{ row.manager.capabilities.join(', ') }}
                </span>
              </template>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="matchScore" label="匹配得分" width="120">
          <template #default="{ row }">
            <el-progress
              :percentage="row.matchScore"
              :color="getScoreColor(row.matchScore)"
              :format="(val) => val.toFixed(1) + '分'"
            />
          </template>
        </el-table-column>

        <el-table-column label="操作" width="120" v-if="matchingForm.mode === 'manual'">
          <template #default="{ row }">
            <el-button link type="primary" @click="showMatchDetail(row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 匹配详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="匹配详情分析"
      width="60%"
    >
      <div v-if="selectedMatch" class="match-detail">
        <el-descriptions title="基础匹配信息" :column="2" border>
          <el-descriptions-item label="客户姓名">
            {{ selectedMatch.customer.name }}
          </el-descriptions-item>
          <el-descriptions-item label="客户经理">
            {{ selectedMatch.manager.name }}
          </el-descriptions-item>
          <el-descriptions-item label="匹配得分">
            {{ selectedMatch.matchScore.toFixed(1) }}分
          </el-descriptions-item>
          <el-descriptions-item label="匹配时间">
            {{ formatDate(selectedMatch.matchTime) }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="match-factors">
          <h4>匹配因素分析</h4>
          <el-progress
            v-for="(factor, index) in selectedMatch.matchFactors"
            :key="index"
            :percentage="factor.weight * 100"
            :format="() => factor.name + ': ' + (factor.weight * 100).toFixed(1) + '%'"
            :color="getFactorColor(factor.weight)"
          />
        </div>

        <div class="match-recommendation">
          <h4>匹配建议</h4>
          <p>{{ selectedMatch.recommendation }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'

// 匹配表单
const matchingForm = reactive({
  mode: 'auto',
  scope: 'unassigned'
})

// 状态变量
const loading = ref(false)
const matching = ref(false)
const detailDialogVisible = ref(false)
const selectedMatch = ref(null)
const matchingResults = ref([])
const availableManagers = ref([])

// 计算属性
const hasMatchResults = computed(() => matchingResults.value.length > 0)

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

// 格式化资产显示
const formatAssets = (value) => {
  return `${value.toFixed(2)}万元`
}

// 格式化日期
const formatDate = (date) => {
  return new Date(date).toLocaleString()
}

// 获取匹配得分颜色
const getScoreColor = (score) => {
  if (score >= 90) return '#67C23A'
  if (score >= 80) return '#409EFF'
  if (score >= 70) return '#E6A23C'
  return '#F56C6C'
}

// 获取因素权重颜色
const getFactorColor = (weight) => {
  if (weight >= 0.8) return '#67C23A'
  if (weight >= 0.6) return '#409EFF'
  if (weight >= 0.4) return '#E6A23C'
  return '#F56C6C'
}

// 开始匹配
const startMatching = async () => {
  matching.value = true
  try {
    const response = await fetch('/api/matching/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(matchingForm)
    })
    
    const data = await response.json()
    if (response.ok) {
      matchingResults.value = data.results
      ElMessage.success('匹配完成')
    } else {
      ElMessage.error(data.message || '匹配失败')
    }
  } catch (error) {
    ElMessage.error('匹配失败：' + error.message)
  } finally {
    matching.value = false
  }
}

// 应用匹配结果
const applyMatching = async () => {
  try {
    const response = await fetch('/api/matching/apply', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        results: matchingResults.value
      })
    })
    
    if (response.ok) {
      ElMessage.success('匹配结果已应用')
      matchingResults.value = []
    } else {
      const data = await response.json()
      ElMessage.error(data.message || '应用匹配结果失败')
    }
  } catch (error) {
    ElMessage.error('应用匹配结果失败：' + error.message)
  }
}

// 导出匹配结果
const exportMatching = () => {
  // 实现导出功能
}

// 显示匹配详情
const showMatchDetail = (match) => {
  selectedMatch.value = {
    ...match,
    matchTime: new Date(),
    matchFactors: [
      { name: '客户需求匹配度', weight: 0.85 },
      { name: '专业能力匹配度', weight: 0.75 },
      { name: '兴趣爱好匹配度', weight: 0.65 },
      { name: '工作负载平衡度', weight: 0.90 }
    ],
    recommendation: '该匹配具有较高的综合得分，客户需求与客户经理的专业能力高度匹配，建议确认此匹配结果。'
  }
  detailDialogVisible.value = true
}

// 获取可用的客户经理列表
const fetchManagers = async () => {
  try {
    const response = await fetch('/api/managers/available')
    const data = await response.json()
    if (response.ok) {
      availableManagers.value = data.managers
    }
  } catch (error) {
    ElMessage.error('获取客户经理列表失败：' + error.message)
  }
}

// 初始化
fetchManagers()
</script>

<style scoped lang="scss">
.matching-container {
  padding: 20px;
  
  .control-card {
    margin-bottom: 20px;
  }
  
  .result-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
  
  .info-cell {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    
    .name {
      font-weight: bold;
    }
    
    .detail {
      color: #909399;
      font-size: 0.9em;
    }
  }
  
  .manager-select {
    width: 200px;
  }
  
  .manager-option {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    small {
      color: #909399;
    }
  }
  
  .match-detail {
    .match-factors {
      margin-top: 20px;
      
      h4 {
        margin-bottom: 16px;
      }
      
      .el-progress {
        margin-bottom: 12px;
      }
    }
    
    .match-recommendation {
      margin-top: 20px;
      
      h4 {
        margin-bottom: 12px;
      }
      
      p {
        color: #606266;
        line-height: 1.6;
      }
    }
  }
}
</style>