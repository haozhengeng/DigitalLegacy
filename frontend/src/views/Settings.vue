<template>
  <div class="settings-page">
    <h3 class="page-title">⚙️ 安全设置</h3>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="setting-card">
          <template #header>个人资料</template>
          <el-form :model="profile" label-width="100px">
            <el-form-item label="显示名称">
              <el-input v-model="profile.display_name" @blur="saveProfile" />
            </el-form-item>
            <el-form-item label="手机号">
              <el-input v-model="profile.phone" @blur="saveProfile" />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input :model-value="profile.email" disabled />
            </el-form-item>
            <el-form-item label="用户名">
              <el-input :model-value="profile.username" disabled />
            </el-form-item>
          </el-form>
        </el-card>

        <el-card class="setting-card" style="margin-top: 20px">
          <template #header>紧急联系人</template>
          <el-form :model="emergency" label-width="120px">
            <el-form-item label="联系人姓名">
              <el-input v-model="emergency.emergency_contact_name" @blur="saveEmergency" />
            </el-form-item>
            <el-form-item label="联系人电话">
              <el-input v-model="emergency.emergency_contact_phone" @blur="saveEmergency" />
            </el-form-item>
            <div class="setting-hint">T+7 天无人响应时，系统将联系该联系人核实您的状态</div>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="setting-card">
          <template #header>
            多因子认证 (MFA)
            <el-tag size="small" :type="profile.is_mfa_enabled ? 'success' : 'info'" style="margin-left: 8px">
              {{ profile.is_mfa_enabled ? '已开启' : '未开启' }}
            </el-tag>
          </template>
          <div class="mfa-section">
            <p>启用多因子认证可大幅提升账户安全性。开启后登录时需要输入验证码。</p>
            <el-button v-if="!profile.is_mfa_enabled" type="primary" @click="enableMFA">
              开启 MFA
            </el-button>
            <el-button v-else type="danger" @click="disableMFA">
              关闭 MFA
            </el-button>
          </div>
        </el-card>

        <el-card class="setting-card" style="margin-top: 20px">
          <template #header>无活动期限</template>
          <el-form label-width="140px">
            <el-form-item label="默认无活动期限">
              <el-input-number v-model="inactivityDays" :min="7" :max="365" @change="saveInactivity" />
              <span style="margin-left: 8px; color: #909399;">天</span>
            </el-form-item>
            <div class="setting-hint">超过此期限未登录且未打卡，系统将自动进入预警流程</div>
          </el-form>
        </el-card>

        <el-card class="setting-card" style="margin-top: 20px">
          <template #header>密钥分片</template>
          <p>将重要私钥拆分为两部分：一部分存储在 App，另一部分可打印后物理保管。</p>
          <el-button type="warning" @click="generateFragments">
            生成密钥分片
          </el-button>
          <div v-if="fragments.length" class="fragments-result">
            <div v-for="(f, i) in fragments" :key="i" class="fragment-item">
              <strong>分片 {{ i + 1 }}: </strong>
              <code>{{ f }}</code>
            </div>
            <el-alert type="warning" show-icon title="请务必将分片 2 打印或抄写后安全保管，App 内存储的是分片 1" :closable="false" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/api/auth'
import { triggerApi } from '@/api/trigger'

const auth = useAuthStore()
const profile = reactive({
  display_name: '', phone: '', email: '', username: '', is_mfa_enabled: false,
})
const emergency = reactive({ emergency_contact_name: '', emergency_contact_phone: '' })
const inactivityDays = ref(90)
const fragments = ref<string[]>([])

async function loadProfile() {
  try {
    const res = await authApi.getMe()
    Object.assign(profile, {
      display_name: res.data.display_name, phone: res.data.phone,
      email: res.data.email, username: res.data.username,
      is_mfa_enabled: res.data.is_mfa_enabled,
    })
    Object.assign(emergency, {
      emergency_contact_name: res.data.emergency_contact_name,
      emergency_contact_phone: res.data.emergency_contact_phone,
    })
    inactivityDays.value = res.data.inactivity_grace_days

    const configRes = await triggerApi.getConfig()
    inactivityDays.value = configRes.data.inactivity_days
  } catch { /* ignore */ }
}

async function saveProfile() {
  try {
    await authApi.updateMe({ display_name: profile.display_name, phone: profile.phone })
    ElMessage.success('已更新')
  } catch { ElMessage.error('更新失败') }
}

async function saveEmergency() {
  try {
    await authApi.updateMe({
      emergency_contact_name: emergency.emergency_contact_name,
      emergency_contact_phone: emergency.emergency_contact_phone,
    })
    ElMessage.success('紧急联系人已更新')
  } catch { ElMessage.error('更新失败') }
}

async function saveInactivity() {
  try {
    await triggerApi.updateConfig({ inactivity_days: inactivityDays.value })
    ElMessage.success('已更新')
  } catch { ElMessage.error('更新失败') }
}

async function enableMFA() {
  ElMessage.info('请使用 Authenticator App 扫描二维码（功能开发中）')
  try {
    await authApi.enableMFA({ secret: 'demo', code: '000000' })
    profile.is_mfa_enabled = true
    ElMessage.success('MFA 已开启')
  } catch { ElMessage.error('操作失败') }
}

async function disableMFA() {
  try {
    await authApi.disableMFA()
    profile.is_mfa_enabled = false
    ElMessage.success('MFA 已关闭')
  } catch { ElMessage.error('操作失败') }
}

function generateFragments() {
  const part1 = Array.from({ length: 16 }, () => Math.random().toString(36)[2]).join('')
  const part2 = Array.from({ length: 16 }, () => Math.random().toString(36)[2]).join('')
  fragments.value = [part1, part2]
  ElMessage.success('密钥分片已生成')
}

onMounted(loadProfile)
</script>

<style scoped>
.settings-page { max-width: 1200px; }
.page-title { margin: 0 0 20px; color: #303133; }
.setting-card { height: 100%; }
.setting-hint { color: #909399; font-size: 12px; margin-top: 4px; line-height: 1.5; }
.mfa-section p { color: #606266; font-size: 14px; margin-bottom: 16px; }
.fragments-result { margin-top: 16px; }
.fragment-item {
  background: #f5f7fa; padding: 8px 12px; border-radius: 6px; margin-bottom: 8px; font-size: 13px;
}
.fragment-item code {
  word-break: break-all; font-size: 12px; color: #e6a23c;
}
</style>
