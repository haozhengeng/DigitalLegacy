<template>
  <div class="trigger-page">
    <div class="page-header">
      <h3 class="page-title">🛡️ 生命开关</h3>
    </div>

    <el-row :gutter="[16, 16]">
      <!-- 左侧：守护状态 + 触发流程时间线 -->
      <el-col :xs="24" :md="16">
        <el-card class="status-card">
          <template #header>
            <span>守护状态</span>
            <el-tag :type="statusInfo.is_emergency_recalled ? 'danger' : statusInfo.is_triggered ? 'warning' : 'success'"
              size="small" style="margin-left: 8px">
              {{ statusInfo.is_emergency_recalled ? '已撤回' : statusInfo.is_triggered ? '触发中' : '守护中' }}
            </el-tag>
          </template>
          <div class="status-body">
            <div class="stage-display">
              <div class="stage-icon">{{ stageIcon }}</div>
              <div class="stage-text">{{ statusInfo.trigger_stage }}</div>
            </div>
            <el-progress
              :percentage="progressPercent"
              :status="progressStatus"
              :stroke-width="16"
              :text-inside="true"
              :format="progressFormat"
            />
            <div class="status-details">
              <div class="detail-item">
                <span class="label">距离上次打卡</span>
                <span class="value">{{ statusInfo.days_since_last_checkin }} 天</span>
              </div>
              <div class="detail-item">
                <span class="label">预设无活动期限</span>
                <span class="value">{{ statusInfo.inactivity_days }} 天</span>
              </div>
              <div class="detail-item" v-if="statusInfo.next_alert_at">
                <span class="label">下次提醒</span>
                <span class="value">{{ statusInfo.next_alert_at }}</span>
              </div>
            </div>
            <div class="status-actions">
              <el-button type="success" size="large" :loading="checkingIn" @click="handleCheckIn">
                <el-icon><Select /></el-icon> 安全打卡
              </el-button>
              <el-button v-if="statusInfo.is_triggered" type="danger" size="large" :loading="recalling" @click="handleRecall">
                <el-icon><Refresh /></el-icon> 紧急撤回
              </el-button>
            </div>
          </div>
        </el-card>

        <el-card class="timeline-card" style="margin-top: 20px">
          <template #header>触发流程</template>
          <el-timeline>
            <el-timeline-item timestamp="T+0 天" placement="top" type="primary">
              <h4>App 强提醒</h4>
              <p v-if="config.alert_t0_push">系统推送通知到您的手机</p>
            </el-timeline-item>
            <el-timeline-item timestamp="T+3 天" placement="top" type="warning">
              <h4>短信 & 语音电话</h4>
              <p v-if="config.alert_t3_sms">发送短信并拨打自动语音电话</p>
            </el-timeline-item>
            <el-timeline-item timestamp="T+7 天" placement="top" type="danger">
              <h4>联系紧急联系人</h4>
              <p v-if="config.alert_t7_contact">通知一级安全联系人进行状态核实</p>
            </el-timeline-item>
            <el-timeline-item timestamp="最终交付" placement="top" type="success">
              <h4>信息分发</h4>
              <p>向受益人发送解锁链接，按权限分配内容</p>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>

      <!-- 右侧：触发配置 + 活动日志 -->
      <el-col :xs="24" :md="8">
        <el-card class="config-card">
          <template #header>触发设置</template>
          <el-form label-width="120px">
            <el-form-item label="启用开关">
              <el-switch v-model="config.is_enabled" @change="saveConfig" />
            </el-form-item>
            <el-form-item label="无活动期限">
              <el-input-number v-model="config.inactivity_days" :min="7" :max="365" @change="saveConfig" />
              <div class="config-hint">天</div>
            </el-form-item>
            <el-form-item label="T+0 推送">
              <el-switch v-model="config.alert_t0_push" @change="saveConfig" />
            </el-form-item>
            <el-form-item label="T+3 短信">
              <el-switch v-model="config.alert_t3_sms" @change="saveConfig" />
            </el-form-item>
            <el-form-item label="T+7 联系人">
              <el-switch v-model="config.alert_t7_contact" @change="saveConfig" />
            </el-form-item>
          </el-form>
        </el-card>

        <el-card class="config-card" style="margin-top: 20px">
          <template #header>活动日志</template>
          <div v-for="log in logs" :key="log.id" class="log-item">
            <el-tag size="small" :type="log.event_type === 'check_in' ? 'success' : 'danger'">
              {{ log.event_type === 'check_in' ? '打卡' : log.event_type === 'emergency_recall' ? '撤回' : log.event_type }}
            </el-tag>
            <span class="log-time">{{ formatTime(log.created_at) }}</span>
          </div>
          <el-empty v-if="!logs.length" description="暂无日志" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { triggerApi, type TriggerConfig, type TriggerStatus, type TriggerLog } from '@/api/trigger'
import { formatDateCN } from '@/utils/time'

const config = ref<TriggerConfig>({
  is_enabled: true, inactivity_days: 90, check_in_interval_days: 90,
  alert_t0_push: true, alert_t3_sms: true, alert_t7_contact: true,
} as TriggerConfig)
const statusInfo = ref<TriggerStatus>({} as TriggerStatus)
const logs = ref<TriggerLog[]>([])
const checkingIn = ref(false)
const recalling = ref(false)

const stageIcon = computed(() => {
  if (statusInfo.value.is_emergency_recalled) return '↩️'
  if (statusInfo.value.is_triggered) return '⚠️'
  return '🛡️'
})

const progressPercent = computed(() => {
  if (!statusInfo.value || !statusInfo.value.inactivity_days) return 0
  const days = statusInfo.value.days_since_last_checkin || 0
  return Math.min(100, Math.round((days / statusInfo.value.inactivity_days) * 100))
})

const progressStatus = computed(() => {
  if (statusInfo.value.is_emergency_recalled) return 'exception'
  if (progressPercent.value >= 100) return 'warning'
  return 'success'
})

function progressFormat(pct: number) {
  if (statusInfo.value.is_emergency_recalled) return '已撤回'
  if (pct >= 100) return '已超期'
  return `剩余 ${statusInfo.value.inactivity_days - (statusInfo.value.days_since_last_checkin || 0)} 天`
}

function formatTime(t: string) {
  return formatDateCN(t)
}

async function loadData() {
  try {
    const [configRes, statusRes, logsRes] = await Promise.all([
      triggerApi.getConfig(), triggerApi.getStatus(), triggerApi.getLogs(),
    ])
    config.value = configRes.data
    statusInfo.value = statusRes.data
    logs.value = logsRes.data
  } catch { /* ignore */ }
}

async function saveConfig() {
  try {
    await triggerApi.updateConfig({
      is_enabled: config.value.is_enabled,
      inactivity_days: config.value.inactivity_days,
      alert_t0_push: config.value.alert_t0_push,
      alert_t3_sms: config.value.alert_t3_sms,
      alert_t7_contact: config.value.alert_t7_contact,
    })
    ElMessage.success('设置已保存')
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '保存失败')
  }
}

async function handleCheckIn() {
  checkingIn.value = true
  try {
    const res = await triggerApi.checkIn()
    ElMessage.success(res.data.message)
    await loadData()
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '打卡失败')
  } finally { checkingIn.value = false }
}

async function handleRecall() {
  await ElMessageBox.confirm('确定要紧急撤回所有触发流程吗？', '紧急撤回', { confirmButtonText: '确认撤回', type: 'warning' })
  recalling.value = true
  try {
    const res = await triggerApi.emergencyRecall()
    ElMessage.success(res.data.message)
    await loadData()
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '撤回失败')
  } finally { recalling.value = false }
}

onMounted(loadData)
</script>

<style scoped>
.trigger-page { max-width: 1200px; }
.page-header { margin-bottom: 20px; }
.page-title { margin: 0; color: #303133; }
.status-card { height: 100%; }
.stage-display {
  text-align: center; padding: 24px 0;
}
.stage-icon { font-size: 56px; margin-bottom: 12px; }
.stage-text { font-size: 20px; font-weight: 600; color: #303133; }
.status-details {
  display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 20px 0;
}
.detail-item {
  background: #f5f7fa; padding: 12px; border-radius: 8px;
}
.detail-item .label { display: block; color: #909399; font-size: 12px; margin-bottom: 4px; }
.detail-item .value { font-size: 18px; font-weight: 600; color: #303133; }
.status-actions {
  display: flex; gap: 12px; justify-content: center; margin-top: 16px;
}
.config-card {
  font-size: 14px;
}
.config-hint {
  display: inline; color: #909399; font-size: 12px; margin-left: 8px;
}
.log-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 0; border-bottom: 1px solid #f0f0f0; font-size: 13px;
}
.log-item:last-child { border-bottom: none; }
.log-time { color: #909399; }

@media (max-width: 768px) {
  .status-details { grid-template-columns: 1fr; }
  .status-actions { flex-direction: column; align-items: stretch; }
  .stage-icon { font-size: 40px; }
  .stage-text { font-size: 17px; }
}
</style>
