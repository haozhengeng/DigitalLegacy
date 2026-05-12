<template>
  <div class="dashboard">
    <!-- 欢迎卡片 + 打卡状态 -->
    <div class="welcome-card">
      <h2>守护你的数字生命</h2>
      <p>数字遗产管家帮你安全托管数字资产，在合适的时机传递给重要的人。</p>
      <div class="checkin-reminder" v-if="status">
        <span v-if="status.days_since_last_checkin === 0">✅ 今日已打卡，一切安好</span>
        <span v-else-if="status.days_since_last_checkin < status.inactivity_days">
          ⏰ 距离下次打卡还有 {{ status.inactivity_days - status.days_since_last_checkin }} 天
        </span>
        <span v-else class="warning">⚠️ 已超过预设期限，请立即打卡</span>
      </div>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="[16, 16]">
      <el-col :xs="12" :sm="12" :md="6" v-for="stat in stats" :key="stat.label">
        <el-card shadow="hover" class="stat-card" @click="$router.push(stat.path)">
          <div class="stat-icon" :style="{ color: stat.color }">{{ stat.icon }}</div>
          <div class="stat-value">{{ stat.count }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近添加 + 快捷操作 -->
    <el-row :gutter="[16, 16]" style="margin-top: 16px">
      <el-col :xs="24" :sm="24" :md="14">
        <el-card class="section-card">
          <template #header>最近添加</template>
          <div class="table-wrapper">
            <el-table :data="recentItems" style="width: 100%" v-loading="loading" stripe size="small">
              <el-table-column prop="title" label="名称" min-width="120" />
              <el-table-column label="分类" width="80">
                <template #default="{ row }">
                  <el-tag :type="tagType(row.category)" size="small">{{ labelMap[row.category] || row.category }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="updated_at" label="时间" width="100">
                <template #default="{ row }">{{ formatDateCN(row.updated_at) }}</template>
              </el-table-column>
            </el-table>
          </div>
          <el-empty v-if="!recentItems.length && !loading" description="暂无数据，前往保险箱添加" />
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="10">
        <el-card class="section-card">
          <template #header>快捷操作</template>
          <div class="quick-actions">
            <el-button type="primary" size="default" class="action-btn" @click="$router.push('/vault')">
              <el-icon><Plus /></el-icon> 添加资产
            </el-button>
            <el-button type="success" size="default" class="action-btn" @click="$router.push('/emotional')">
              <el-icon><Plus /></el-icon> 写封信
            </el-button>
            <el-button type="warning" size="default" class="action-btn" @click="$router.push('/beneficiaries')">
              <el-icon><Plus /></el-icon> 添加受益人
            </el-button>
            <el-button size="default" class="action-btn" style="background:#6b7c93;color:#fff" @click="$router.push('/trigger')">
              <el-icon><Select /></el-icon> 安全打卡
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { vaultApi } from '@/api/vault'
import { beneficiariesApi } from '@/api/beneficiaries'
import { emotionalApi } from '@/api/emotional'
import { triggerApi, type TriggerStatus } from '@/api/trigger'
import { formatDateCN } from '@/utils/time'

const loading = ref(false)
const recentItems = ref<any[]>([])
const status = ref<TriggerStatus | null>(null)
const stats = ref([
  { label: '保险箱条目', icon: '🔐', count: 0, color: '#409eff', path: '/vault' },
  { label: '情感档案', icon: '💌', count: 0, color: '#e6a23c', path: '/emotional' },
  { label: '受益人', icon: '👨‍👩‍👧', count: 0, color: '#67c23a', path: '/beneficiaries' },
  { label: '守护天数', icon: '🛡️', count: 0, color: '#909399', path: '/trigger' },
])

const labelMap: Record<string, string> = {
  bank: '银行', crypto: '加密货币', insurance: '保险',
  social: '社交', email: '邮箱', cloud: '云服务',
  subscription: '订阅', instruction: '指令', other: '其他',
}

function tagType(cat: string) {
  const m: Record<string, string> = {
    bank: 'success', crypto: 'danger', insurance: 'warning',
    social: 'primary', email: 'info', cloud: '',
    instruction: 'danger', subscription: 'warning',
  }
  return m[cat] || 'info'
}

async function loadData() {
  loading.value = true
  try {
    const [vaultRes, benRes, emoRes, statusRes] = await Promise.all([
      vaultApi.list(), beneficiariesApi.list(), emotionalApi.list(), triggerApi.getStatus(),
    ])
    recentItems.value = vaultRes.data.slice(0, 5)
    stats.value[0].count = vaultRes.data.length
    stats.value[1].count = emoRes.data.length
    stats.value[2].count = benRes.data.length
    status.value = statusRes.data
    stats.value[3].count = statusRes.data.days_since_last_checkin ?? '-'
  } catch { /* ignore */ }
  finally { loading.value = false }
}

onMounted(loadData)
</script>

<style scoped>
.dashboard { max-width: 1200px; }
.welcome-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
}
.welcome-card h2 { margin: 0 0 8px; font-size: 24px; }
.welcome-card p { margin: 0; opacity: 0.9; font-size: 14px; }
.checkin-reminder {
  margin-top: 16px;
  background: rgba(255,255,255,0.2);
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
}
.checkin-reminder .warning { color: #ffd700; font-weight: 600; }
.stat-card {
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s;
}
.stat-card:hover { transform: translateY(-2px); }
.stat-icon { font-size: 28px; margin-bottom: 8px; }
.stat-value { font-size: 32px; font-weight: 700; color: #303133; }
.stat-label { margin-top: 4px; color: #909399; font-size: 13px; }
.section-card { height: 100%; }
.quick-actions { display: flex; flex-direction: column; gap: 12px; }
.action-btn { width: 100%; }
.table-wrapper { overflow-x: auto; }

@media (max-width: 768px) {
  .welcome-card { padding: 20px; border-radius: 12px; margin-bottom: 16px; }
  .welcome-card h2 { font-size: 20px; }
  .welcome-card p { font-size: 13px; }
  .checkin-reminder { font-size: 13px; padding: 8px 12px; }
  .stat-value { font-size: 24px; }
  .stat-icon { font-size: 22px; }
}
</style>
