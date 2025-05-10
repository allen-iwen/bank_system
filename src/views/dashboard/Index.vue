<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <!-- 统计卡片 -->
      <el-col :span="6" v-for="(card, index) in statisticsCards" :key="index">
        <el-card shadow="hover" class="statistics-card">
          <div class="card-icon" :style="{ backgroundColor: card.color }">
            <el-icon><component :is="card.icon" /></el-icon>
          </div>
          <div class="card-content">
            <div class="card-title">{{ card.title }}</div>
            <div class="card-value">{{ card.value }}</div>
            <div class="card-change" :class="card.trend">
              <el-icon><component :is="card.trend === 'up' ? 'ArrowUp' : 'ArrowDown'" /></el-icon>
              {{ card.change }}%
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <!-- 客户分布图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>客户分类分布</span>
              <el-radio-group v-model="customerChartType" size="small">
                <el-radio-button label="pie">饼图</el-radio-button>
                <el-radio-button label="bar">柱状图</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart" ref="customerChartRef"></div>
        </el-card>
      </el-col>

      <!-- 匹配趋势图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>匹配效果趋势</span>
              <el-select v-model="matchingPeriod" size="small">
                <el-option label="最近7天" value="7" />
                <el-option label="最近30天" value="30" />
                <el-option label="最近90天" value="90" />
              </el-select>
            </div>
          </template>
          <div class="chart" ref="matchingChartRef"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <!-- 客户经理业绩排行 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>客户经理业绩排行</span>
              <el-button-group size="small">
                <el-button type="primary" plain>客户数量</el-button>
                <el-button>客户资产</el-button>
              </el-button-group>
            </div>
          </template>
          <div class="ranking-list">
            <div v-for="(manager, index) in managerRankings" :key="index" class="ranking-item">
              <span class="ranking-index" :class="{ 'top-three': index < 3 }">{{ index + 1 }}</span>
              <el-avatar :size="32" :src="manager.avatar" />
              <span class="manager-name">{{ manager.name }}</span>
              <span class="manager-value">{{ manager.value }}</span>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 最新匹配记录 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>最新匹配记录</span>
              <el-button type="primary" link>查看全部</el-button>
            </div>
          </template>
          <el-table :data="latestMatches" style="width: 100%">
            <el-table-column prop="time" label="时间" width="150" />
            <el-table-column prop="customer" label="客户" />
            <el-table-column prop="manager" label="客户经理" />
            <el-table-column prop="score" label="匹配得分" width="100">
              <template #default="{ row }">
                <el-tag :type="getScoreTagType(row.score)">{{ row.score }}分</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { User, Money, Connection, DataLine, ArrowUp, ArrowDown } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// 统计卡片数据
const statisticsCards = reactive([
  {
    title: '总客户数',
    value: '1,234',
    change: '15.4',
    trend: 'up',
    icon: 'User',
    color: '#409EFF'
  },
  {
    title: '总资产规模',
    value: '￥8.56亿',
    change: '12.3',
    trend: 'up',
    icon: 'Money',
    color: '#67C23A'
  },
  {
    title: '本月新增匹配',
    value: '89',
    change: '8.5',
    trend: 'up',
    icon: 'Connection',
    color: '#E6A23C'
  },
  {
    title: '平均匹配分',
    value: '85.6',
    change: '2.1',
    trend: 'down',
    icon: 'DataLine',
    color: '#F56C6C'
  }
])

// 客户分布图
const customerChartRef = ref(null)
const customerChartType = ref('pie')
let customerChart = null

// 匹配趋势图
const matchingChartRef = ref(null)
const matchingPeriod = ref('7')
let matchingChart = null

// 客户经理排行榜
const managerRankings = reactive([
  { name: '张经理', value: '126位客户', avatar: '' },
  { name: '李经理', value: '98位客户', avatar: '' },
  { name: '王经理', value: '87位客户', avatar: '' },
  { name: '赵经理', value: '76位客户', avatar: '' },
  { name: '刘经理', value: '65位客户', avatar: '' }
])

// 最新匹配记录
const latestMatches = reactive([
  { time: '2023-08-15 14:30', customer: '张三', manager: '李经理', score: 92 },
  { time: '2023-08-15 11:20', customer: '李四', manager: '王经理', score: 88 },
  { time: '2023-08-15 10:15', customer: '王五', manager: '张经理', score: 85 },
  { time: '2023-08-15 09:30', customer: '赵六', manager: '刘经理', score: 78 }
])

// 初始化图表
onMounted(() => {
  initCustomerChart()
  initMatchingChart()
})

// 初始化客户分布图
const initCustomerChart = () => {
  customerChart = echarts.init(customerChartRef.value)
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center'
    },
    series: [
      {
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '16',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: 335, name: 'A类客户' },
          { value: 310, name: 'B类客户' },
          { value: 234, name: 'C类客户' },
          { value: 135, name: 'D类客户' },
          { value: 148, name: 'E类客户' }
        ]
      }
    ]
  }
  customerChart.setOption(option)
}

// 初始化匹配趋势图
const initMatchingChart = () => {
  matchingChart = echarts.init(matchingChartRef.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: {
      type: 'value',
      name: '匹配分数'
    },
    series: [
      {
        data: [85, 88, 92, 87, 90, 93, 89],
        type: 'line',
        smooth: true,
        areaStyle: {}
      }
    ]
  }
  matchingChart.setOption(option)
}

// 获取匹配分数对应的标签类型
const getScoreTagType = (score) => {
  if (score >= 90) return 'success'
  if (score >= 80) return ''
  if (score >= 70) return 'warning'
  return 'danger'
}
</script>

<style scoped lang="scss">
.dashboard-container {
  padding: 20px;
  
  .statistics-card {
    display: flex;
    align-items: center;
    padding: 20px;
    
    .card-icon {
      width: 48px;
      height: 48px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 16px;
      
      .el-icon {
        font-size: 24px;
        color: #fff;
      }
    }
    
    .card-content {
      flex: 1;
      
      .card-title {
        font-size: 14px;
        color: #909399;
        margin-bottom: 8px;
      }
      
      .card-value {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 8px;
      }
      
      .card-change {
        font-size: 12px;
        display: flex;
        align-items: center;
        
        &.up {
          color: #67C23A;
        }
        
        &.down {
          color: #F56C6C;
        }
        
        .el-icon {
          margin-right: 4px;
        }
      }
    }
  }
  
  .chart-row {
    margin-top: 20px;
  }
  
  .chart-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .chart {
      height: 300px;
    }
  }
  
  .ranking-list {
    .ranking-item {
      display: flex;
      align-items: center;
      padding: 12px 0;
      border-bottom: 1px solid #EBEEF5;
      
      &:last-child {
        border-bottom: none;
      }
      
      .ranking-index {
        width: 24px;
        height: 24px;
        line-height: 24px;
        text-align: center;
        border-radius: 50%;
        background-color: #F2F6FC;
        margin-right: 12px;
        
        &.top-three {
          color: #fff;
          background-color: #E6A23C;
          
          &:first-child {
            background-color: #F56C6C;
          }
          
          &:nth-child(2) {
            background-color: #E6A23C;
          }
          
          &:nth-child(3) {
            background-color: #409EFF;
          }
        }
      }
      
      .el-avatar {
        margin-right: 12px;
      }
      
      .manager-name {
        flex: 1;
      }
      
      .manager-value {
        color: #409EFF;
        font-weight: bold;
      }
    }
  }
}
</style>