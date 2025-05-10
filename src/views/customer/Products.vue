<template>
  <div class="customer-products">
    <el-card class="page-header">
      <h1>金融产品中心</h1>
      <p>发现适合您的各种金融产品</p>
    </el-card>
    
    <el-row :gutter="20">
      <el-col :span="18">
        <el-tabs v-model="activeTab" class="product-tabs">
          <el-tab-pane label="存款产品" name="deposit">
            <el-card class="tab-content">
              <el-table :data="depositProducts" style="width: 100%">
                <el-table-column prop="name" label="产品名称" width="180" />
                <el-table-column prop="rate" label="年利率" width="100" />
                <el-table-column prop="minAmount" label="起存金额" width="120" />
                <el-table-column prop="term" label="期限" width="120" />
                <el-table-column prop="description" label="产品描述" />
                <el-table-column label="操作" width="120">
                  <template #default>
                    <el-button type="primary" size="small">购买</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-tab-pane>
          
          <el-tab-pane label="理财产品" name="wealth">
            <el-card class="tab-content">
              <el-table :data="wealthProducts" style="width: 100%">
                <el-table-column prop="name" label="产品名称" width="180" />
                <el-table-column prop="expectedReturn" label="预期年化收益" width="140" />
                <el-table-column prop="riskLevel" label="风险等级" width="100">
                  <template #default="scope">
                    <el-tag :type="getRiskTypeColor(scope.row.riskLevel)">
                      {{ scope.row.riskLevel }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="minAmount" label="起购金额" width="120" />
                <el-table-column prop="term" label="投资期限" width="120" />
                <el-table-column label="操作" width="120">
                  <template #default>
                    <el-button type="primary" size="small">购买</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-tab-pane>
          
          <el-tab-pane label="贷款产品" name="loan">
            <el-card class="tab-content">
              <el-table :data="loanProducts" style="width: 100%">
                <el-table-column prop="name" label="产品名称" width="180" />
                <el-table-column prop="rate" label="年利率" width="100" />
                <el-table-column prop="maxAmount" label="最高额度" width="120" />
                <el-table-column prop="term" label="最长期限" width="120" />
                <el-table-column prop="description" label="产品描述" />
                <el-table-column label="操作" width="120">
                  <template #default>
                    <el-button type="primary" size="small">申请</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-tab-pane>
          
          <el-tab-pane label="基金产品" name="fund">
            <el-card class="tab-content">
              <el-table :data="fundProducts" style="width: 100%">
                <el-table-column prop="name" label="产品名称" width="180" />
                <el-table-column prop="type" label="基金类型" width="120" />
                <el-table-column prop="returnRate" label="近一年收益率" width="140" />
                <el-table-column prop="riskLevel" label="风险等级" width="100">
                  <template #default="scope">
                    <el-tag :type="getRiskTypeColor(scope.row.riskLevel)">
                      {{ scope.row.riskLevel }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="minAmount" label="起购金额" width="120" />
                <el-table-column label="操作" width="120">
                  <template #default>
                    <el-button type="primary" size="small">购买</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-tab-pane>
        </el-tabs>
      </el-col>
      
      <el-col :span="6">
        <el-card class="filter-card">
          <template #header>
            <div class="card-header">
              <h3>筛选条件</h3>
            </div>
          </template>
          
          <el-form label-position="top">
            <el-form-item label="产品类型">
              <el-select v-model="filterType" placeholder="选择产品类型" style="width: 100%">
                <el-option label="全部" value="" />
                <el-option label="存款产品" value="deposit" />
                <el-option label="理财产品" value="wealth" />
                <el-option label="贷款产品" value="loan" />
                <el-option label="基金产品" value="fund" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="风险等级">
              <el-select v-model="filterRisk" placeholder="选择风险等级" style="width: 100%">
                <el-option label="全部" value="" />
                <el-option label="低风险" value="低风险" />
                <el-option label="中低风险" value="中低风险" />
                <el-option label="中风险" value="中风险" />
                <el-option label="中高风险" value="中高风险" />
                <el-option label="高风险" value="高风险" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="期限">
              <el-select v-model="filterTerm" placeholder="选择期限" style="width: 100%">
                <el-option label="全部" value="" />
                <el-option label="3个月以内" value="3" />
                <el-option label="3-6个月" value="6" />
                <el-option label="6-12个月" value="12" />
                <el-option label="1-3年" value="36" />
                <el-option label="3年以上" value="37" />
              </el-select>
            </el-form-item>
            
            <el-button type="primary" style="width: 100%">应用筛选</el-button>
            <el-button style="width: 100%; margin-top: 10px">重置</el-button>
          </el-form>
        </el-card>
        
        <el-card class="hot-products-card">
          <template #header>
            <div class="card-header">
              <h3>热门产品</h3>
            </div>
          </template>
          
          <div v-for="product in hotProducts" :key="product.id" class="hot-product-item">
            <h4>{{ product.name }}</h4>
            <p>{{ product.description }}</p>
            <div class="hot-product-rate">
              <span>{{ product.rate }}</span>
              <el-button type="text" size="small">查看详情</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('deposit')
const filterType = ref('')
const filterRisk = ref('')
const filterTerm = ref('')

// 存款产品数据
const depositProducts = ref([
  {
    id: 1,
    name: '定期存款-三个月',
    rate: '2.1%',
    minAmount: '¥5,000',
    term: '3个月',
    description: '稳健的短期定期存款，到期自动转存'
  },
  {
    id: 2,
    name: '定期存款-六个月',
    rate: '2.6%',
    minAmount: '¥5,000',
    term: '6个月',
    description: '稳健的中期定期存款，到期自动转存'
  },
  {
    id: 3,
    name: '定期存款-一年',
    rate: '3.1%',
    minAmount: '¥5,000',
    term: '12个月',
    description: '稳健的长期定期存款，到期自动转存'
  },
  {
    id: 4,
    name: '活期存款',
    rate: '0.3%',
    minAmount: '¥0',
    term: '灵活',
    description: '随存随取的活期存款，灵活方便'
  }
])

// 理财产品数据
const wealthProducts = ref([
  {
    id: 1,
    name: '稳健理财-周周盈',
    expectedReturn: '3.8%',
    riskLevel: '低风险',
    minAmount: '¥10,000',
    term: '7天',
    description: '短期理财产品，每周开放申购和赎回'
  },
  {
    id: 2,
    name: '结构性存款-汇升A',
    expectedReturn: '3.2%-5.5%',
    riskLevel: '中低风险',
    minAmount: '¥50,000',
    term: '6个月',
    description: '挂钩利率的结构性存款，收益浮动'
  },
  {
    id: 3,
    name: '现金管理类理财产品',
    expectedReturn: '3.0%',
    riskLevel: '低风险',
    minAmount: '¥1,000',
    term: '随时',
    description: '类似货币基金，可随时申购赎回'
  }
])

// 贷款产品数据
const loanProducts = ref([
  {
    id: 1,
    name: '个人消费贷款',
    rate: '4.8%',
    maxAmount: '¥300,000',
    term: '3年',
    description: '用于个人消费的信用贷款，无需抵押'
  },
  {
    id: 2,
    name: '房屋抵押贷款',
    rate: '4.1%',
    maxAmount: '¥5,000,000',
    term: '30年',
    description: '以房产作为抵押的长期贷款'
  },
  {
    id: 3,
    name: '汽车贷款',
    rate: '4.5%',
    maxAmount: '¥500,000',
    term: '5年',
    description: '用于购买汽车的专项贷款'
  }
])

// 基金产品数据
const fundProducts = ref([
  {
    id: 1,
    name: '恒盛成长混合型基金',
    type: '混合型',
    returnRate: '15.6%',
    riskLevel: '中高风险',
    minAmount: '¥1,000'
  },
  {
    id: 2,
    name: '恒盛债券优选',
    type: '债券型',
    returnRate: '8.2%',
    riskLevel: '中低风险',
    minAmount: '¥1,000'
  },
  {
    id: 3,
    name: '恒盛货币市场基金',
    type: '货币型',
    returnRate: '3.5%',
    riskLevel: '低风险',
    minAmount: '¥1'
  },
  {
    id: 4,
    name: '恒盛中证500指数基金',
    type: '指数型',
    returnRate: '12.8%',
    riskLevel: '中风险',
    minAmount: '¥1,000'
  }
])

// 热门产品数据
const hotProducts = ref([
  {
    id: 1,
    name: '恒盛成长混合型基金',
    description: '精选优质成长型企业',
    rate: '近一年收益率: 15.6%'
  },
  {
    id: 2,
    name: '结构性存款-汇升A',
    description: '挂钩利率的结构性存款',
    rate: '预期收益率: 3.2%-5.5%'
  },
  {
    id: 3,
    name: '定期存款-一年',
    description: '稳健的长期定期存款',
    rate: '年利率: 3.1%'
  }
])

// 获取风险等级对应的标签颜色
const getRiskTypeColor = (riskLevel) => {
  const riskMap = {
    '低风险': 'success',
    '中低风险': 'info',
    '中风险': '',
    '中高风险': 'warning',
    '高风险': 'danger'
  }
  return riskMap[riskLevel] || ''
}
</script>

<style scoped>
.customer-products {
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

.product-tabs {
  margin-bottom: 20px;
}

.tab-content {
  padding: 10px;
}

.filter-card,
.hot-products-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  font-size: 16px;
  margin: 0;
  color: #303133;
}

.hot-product-item {
  border-bottom: 1px solid #EBEEF5;
  padding: 10px 0;
}

.hot-product-item:last-child {
  border-bottom: none;
}

.hot-product-item h4 {
  margin: 0 0 5px 0;
  color: #303133;
  font-size: 14px;
}

.hot-product-item p {
  margin: 0 0 5px 0;
  color: #606266;
  font-size: 12px;
}

.hot-product-rate {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hot-product-rate span {
  color: #F56C6C;
  font-weight: bold;
  font-size: 13px;
}
</style> 