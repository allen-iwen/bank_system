<template>
  <div class="customer-profile">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="8" :lg="6">
        <el-card class="profile-card">
          <div class="profile-avatar">
            <el-avatar :size="120" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"></el-avatar>
            <h2>张晓明</h2>
            <p>普通客户</p>
            <el-button type="primary">修改资料</el-button>
          </div>
          <el-divider></el-divider>
          <div class="profile-info">
            <div class="info-item">
              <span class="label">客户等级</span>
              <span class="value">黄金客户</span>
            </div>
            <div class="info-item">
              <span class="label">客户经理</span>
              <span class="value">王经理</span>
            </div>
            <div class="info-item">
              <span class="label">开户时间</span>
              <span class="value">2020-06-15</span>
            </div>
            <div class="info-item">
              <span class="label">上次登录</span>
              <span class="value">2023-05-10 14:30:22</span>
            </div>
          </div>
        </el-card>
        
        <el-card class="contact-card">
          <template #header>
            <div class="card-header">
              <h3>联系信息</h3>
              <el-button type="text">编辑</el-button>
            </div>
          </template>
          <div class="contact-info">
            <div class="info-item">
              <i class="el-icon-phone"></i>
              <span>手机号码：138****6666</span>
            </div>
            <div class="info-item">
              <i class="el-icon-message"></i>
              <span>电子邮箱：zhang****@email.com</span>
            </div>
            <div class="info-item">
              <i class="el-icon-map-location"></i>
              <span>联系地址：北京市海淀区中关村大街1号</span>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="24" :md="16" :lg="18">
        <el-card class="account-card">
          <template #header>
            <div class="card-header">
              <h3>我的账户</h3>
              <el-button type="text">查看全部</el-button>
            </div>
          </template>
          <el-row :gutter="20" class="account-summary">
            <el-col :xs="24" :sm="8">
              <div class="account-item">
                <div class="account-title">总资产(元)</div>
                <div class="account-amount">158,625.50</div>
                <div class="account-trend up">
                  <i class="el-icon-top"></i>
                  <span>5.8%</span>
                </div>
              </div>
            </el-col>
            <el-col :xs="24" :sm="8">
              <div class="account-item">
                <div class="account-title">总负债(元)</div>
                <div class="account-amount">42,300.00</div>
                <div class="account-trend down">
                  <i class="el-icon-bottom"></i>
                  <span>2.1%</span>
                </div>
              </div>
            </el-col>
            <el-col :xs="24" :sm="8">
              <div class="account-item">
                <div class="account-title">净资产(元)</div>
                <div class="account-amount">116,325.50</div>
                <div class="account-trend up">
                  <i class="el-icon-top"></i>
                  <span>8.3%</span>
                </div>
              </div>
            </el-col>
          </el-row>
          <el-divider></el-divider>
          <div class="account-list">
            <div class="account-list-item" v-for="account in accounts" :key="account.id">
              <div class="account-info">
                <div class="account-name">{{ account.name }}</div>
                <div class="account-number">{{ account.accountNumber }}</div>
              </div>
              <div class="account-balance">
                <div class="balance-amount">{{ account.balance }}</div>
                <div class="balance-label">{{ account.currency }}</div>
              </div>
            </div>
          </div>
        </el-card>
        
        <el-card class="transactions-card">
          <template #header>
            <div class="card-header">
              <h3>最近交易</h3>
              <el-button type="text">查看全部</el-button>
            </div>
          </template>
          <el-table :data="transactions" style="width: 100%">
            <el-table-column prop="date" label="交易日期" width="160" />
            <el-table-column prop="description" label="交易描述" />
            <el-table-column prop="account" label="账户" width="180" />
            <el-table-column prop="amount" label="交易金额" width="120">
              <template #default="scope">
                <span :class="scope.row.amount.startsWith('-') ? 'amount-negative' : 'amount-positive'">
                  {{ scope.row.amount }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="balance" label="余额" width="120" />
          </el-table>
        </el-card>
        
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
            <el-card class="financial-goals-card">
              <template #header>
                <div class="card-header">
                  <h3>财务目标</h3>
                  <el-button type="text">管理</el-button>
                </div>
              </template>
              <div class="goal-list">
                <div class="goal-item" v-for="goal in financialGoals" :key="goal.id">
                  <div class="goal-info">
                    <h4>{{ goal.name }}</h4>
                    <p>目标：{{ goal.target }} | 时限：{{ goal.timeframe }}</p>
                  </div>
                  <el-progress :percentage="goal.progress" :color="goal.color"></el-progress>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :xs="24" :sm="12">
            <el-card class="appointments-card">
              <template #header>
                <div class="card-header">
                  <h3>预约和提醒</h3>
                  <el-button type="text">新增</el-button>
                </div>
              </template>
              <el-timeline>
                <el-timeline-item
                  v-for="appointment in appointments"
                  :key="appointment.id"
                  :timestamp="appointment.date"
                  :type="appointment.type"
                >
                  {{ appointment.title }}
                  <p>{{ appointment.description }}</p>
                </el-timeline-item>
              </el-timeline>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 账户数据
const accounts = ref([
  {
    id: 1,
    name: '活期储蓄账户',
    accountNumber: '6222 **** **** 1234',
    balance: '45,280.35',
    currency: 'CNY'
  },
  {
    id: 2,
    name: '定期存款账户',
    accountNumber: '6222 **** **** 5678',
    balance: '100,000.00',
    currency: 'CNY'
  },
  {
    id: 3,
    name: '投资理财账户',
    accountNumber: '6222 **** **** 9012',
    balance: '13,345.15',
    currency: 'CNY'
  }
])

// 交易数据
const transactions = ref([
  {
    id: 1,
    date: '2023-05-10 14:22:36',
    description: '工资转入',
    account: '活期储蓄账户',
    amount: '+8,500.00',
    balance: '45,280.35'
  },
  {
    id: 2,
    date: '2023-05-09 09:15:20',
    description: '购买基金产品',
    account: '投资理财账户',
    amount: '-2,000.00',
    balance: '13,345.15'
  },
  {
    id: 3,
    date: '2023-05-08 18:30:45',
    description: '超市消费',
    account: '活期储蓄账户',
    amount: '-356.80',
    balance: '36,780.35'
  },
  {
    id: 4,
    date: '2023-05-07 12:24:10',
    description: '定期存款利息',
    account: '活期储蓄账户',
    amount: '+1,250.00',
    balance: '37,137.15'
  },
  {
    id: 5,
    date: '2023-05-05 20:13:18',
    description: '网上购物',
    account: '活期储蓄账户',
    amount: '-1,280.50',
    balance: '35,887.15'
  }
])

// 财务目标数据
const financialGoals = ref([
  {
    id: 1,
    name: '购买新车',
    target: '200,000元',
    timeframe: '2年',
    progress: 45,
    color: '#409EFF'
  },
  {
    id: 2,
    name: '子女教育金',
    target: '500,000元',
    timeframe: '10年',
    progress: 28,
    color: '#67C23A'
  },
  {
    id: 3,
    name: '退休储蓄',
    target: '2,000,000元',
    timeframe: '30年',
    progress: 15,
    color: '#E6A23C'
  }
])

// 预约和提醒数据
const appointments = ref([
  {
    id: 1,
    title: '贷款到期还款',
    description: '个人消费贷款将于下周到期，请确保账户资金充足',
    date: '2023-05-15',
    type: 'warning'
  },
  {
    id: 2,
    title: '理财产品到期',
    description: '您购买的"季享盈"理财产品即将到期',
    date: '2023-05-20',
    type: 'success'
  },
  {
    id: 3,
    title: '客户经理预约',
    description: '王经理预约您讨论投资组合调整建议',
    date: '2023-05-25 15:00',
    type: 'primary'
  }
])
</script>

<style scoped>
.customer-profile {
  padding: 20px;
}

.profile-card,
.contact-card,
.account-card,
.transactions-card,
.financial-goals-card,
.appointments-card {
  margin-bottom: 20px;
}

.profile-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.profile-avatar h2 {
  margin: 15px 0 5px;
  font-size: 18px;
}

.profile-avatar p {
  margin: 0 0 15px;
  color: #909399;
}

.profile-info,
.contact-info {
  padding: 0 10px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #EBEEF5;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item .label {
  color: #909399;
}

.info-item .value {
  font-weight: 500;
}

.contact-info .info-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

.contact-info .info-item i {
  margin-right: 10px;
  color: #909399;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.account-summary {
  padding: 10px 0;
}

.account-item {
  background-color: #F5F7FA;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.account-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.account-amount {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 10px;
}

.account-trend {
  font-size: 14px;
  display: flex;
  align-items: center;
}

.account-trend.up {
  color: #67C23A;
}

.account-trend.down {
  color: #F56C6C;
}

.account-trend i {
  margin-right: 5px;
}

.account-list-item {
  display: flex;
  justify-content: space-between;
  padding: 15px 0;
  border-bottom: 1px solid #EBEEF5;
}

.account-list-item:last-child {
  border-bottom: none;
}

.account-name {
  font-weight: 500;
  margin-bottom: 5px;
}

.account-number {
  font-size: 12px;
  color: #909399;
}

.balance-amount {
  font-weight: 500;
  text-align: right;
  margin-bottom: 5px;
}

.balance-label {
  font-size: 12px;
  color: #909399;
  text-align: right;
}

.amount-positive {
  color: #67C23A;
}

.amount-negative {
  color: #F56C6C;
}

.goal-item {
  margin-bottom: 20px;
}

.goal-info {
  margin-bottom: 10px;
}

.goal-info h4 {
  margin: 0 0 5px 0;
  font-size: 14px;
}

.goal-info p {
  margin: 0;
  font-size: 12px;
  color: #909399;
}
</style> 