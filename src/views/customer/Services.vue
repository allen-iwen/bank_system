<template>
  <div class="customer-services">
    <el-card class="page-header">
      <h1>我的金融服务</h1>
      <p>查看并管理您的所有银行服务</p>
    </el-card>
    
    <el-row :gutter="20" class="service-cards">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="service in services" :key="service.id">
        <el-card class="service-card" :body-style="{ padding: '0px' }">
          <div class="service-icon" :style="{ backgroundColor: service.color }">
            <i :class="service.icon"></i>
          </div>
          <div class="service-content">
            <h3>{{ service.name }}</h3>
            <p>{{ service.description }}</p>
            <el-button type="primary" text>查看详情</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card class="recommendations-card">
      <template #header>
        <div class="card-header">
          <h2>为您推荐的服务</h2>
        </div>
      </template>
      <el-table :data="recommendations" style="width: 100%">
        <el-table-column prop="name" label="产品名称" />
        <el-table-column prop="type" label="类型" />
        <el-table-column prop="rate" label="利率/收益率" />
        <el-table-column prop="term" label="期限" />
        <el-table-column label="操作">
          <template #default>
            <el-button type="primary" size="small">了解详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 客户服务数据
const services = ref([
  {
    id: 1,
    name: '个人存款',
    description: '查看和管理您的活期和定期存款账户',
    icon: 'el-icon-money',
    color: '#67C23A'
  },
  {
    id: 2,
    name: '理财产品',
    description: '浏览和购买适合您风险偏好的理财产品',
    icon: 'el-icon-pie-chart',
    color: '#409EFF'
  },
  {
    id: 3,
    name: '贷款服务',
    description: '查看您的贷款情况和还款计划',
    icon: 'el-icon-house',
    color: '#E6A23C'
  },
  {
    id: 4,
    name: '信用卡',
    description: '管理您的信用卡账单和额度',
    icon: 'el-icon-credit-card',
    color: '#F56C6C'
  },
  {
    id: 5,
    name: '基金投资',
    description: '了解基金投资情况和收益',
    icon: 'el-icon-data-line',
    color: '#9B59B6'
  },
  {
    id: 6,
    name: '保险服务',
    description: '查看您的保险保障情况',
    icon: 'el-icon-umbrella',
    color: '#3498DB'
  }
])

// 推荐产品数据
const recommendations = ref([
  {
    name: '稳健理财-季享盈',
    type: '固收类',
    rate: '4.2%',
    term: '3个月'
  },
  {
    name: '结构性存款-汇升利',
    type: '混合类',
    rate: '1.5%-5.8%',
    term: '6个月'
  },
  {
    name: '新兴市场债券基金',
    type: '债券基金',
    rate: '6.5%（近一年）',
    term: '灵活'
  }
])
</script>

<style scoped>
.customer-services {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  font-size: 24px;
  margin: 0 0 10px 0;
  color: #303133;
}

.page-header p {
  color: #606266;
  margin: 0;
}

.service-cards {
  margin-bottom: 20px;
}

.service-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.service-card:hover {
  transform: translateY(-5px);
}

.service-icon {
  height: 120px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
}

.service-icon i {
  font-size: 40px;
}

.service-content {
  padding: 15px;
}

.service-content h3 {
  margin: 0 0 10px 0;
  color: #303133;
}

.service-content p {
  color: #606266;
  margin: 0 0 15px 0;
  height: 40px;
}

.recommendations-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recommendations-card h2 {
  font-size: 18px;
  margin: 0;
  color: #303133;
}
</style> 