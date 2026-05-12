<template>
  <div class="emotional-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h3 class="page-title">💌 情感档案</h3>
      <el-button type="primary" @click="showDialog = true">
        <el-icon><Plus /></el-icon> 创建档案
      </el-button>
    </div>

    <!-- 情感档案卡片列表 -->
    <el-row :gutter="[16, 16]">
      <el-col :xs="24" :sm="12" :md="8" v-for="item in list" :key="item.id">
        <el-card shadow="hover" class="emo-card">
          <div class="emo-icon">
            {{ item.file_type === 'letter' ? '📝' : item.file_type === 'voice' ? '🎤' : item.file_type === 'video' ? '🎬' : '📁' }}
          </div>
          <div class="emo-title">{{ item.title }}</div>
          <div class="emo-meta">
            <el-tag size="small" :type="fileType(item.file_type)">{{ fileLabel(item.file_type) }}</el-tag>
            <el-tag v-if="item.is_delivered" size="small" type="success">已送达</el-tag>
            <el-tag v-else size="small" type="info">待交付</el-tag>
          </div>
          <div class="emo-footer">
            <el-button text type="primary" size="small" @click="editItem(item)">编辑</el-button>
            <el-button text type="danger" size="small" @click="handleDelete(item)">删除</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-empty v-if="!list.length" description="暂无情感档案，为重要的人留下一些话吧" />

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="showDialog" :title="editingId ? '编辑档案' : '创建情感档案'" width="550px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="例如：给妻子的最后一封信" />
        </el-form-item>
        <el-form-item label="类型" prop="file_type">
          <el-select v-model="form.file_type">
            <el-option label="信件" value="letter" />
            <el-option label="语音" value="voice" />
            <el-option label="视频" value="video" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="内容" prop="encrypted_content">
          <el-input v-model="form.encrypted_content" type="textarea" :rows="8"
            placeholder="写下你想对重要的人说的话…" />
        </el-form-item>
        <el-form-item label="指定受益人">
          <el-select v-model="form.recipient_beneficiary_id" placeholder="留空则所有受益人可查看" clearable>
            <el-option v-for="b in beneficiaries" :key="b.id" :label="b.name" :value="b.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { emotionalApi, type EmotionalFile } from '@/api/emotional'
import { beneficiariesApi, type Beneficiary } from '@/api/beneficiaries'

const list = ref<EmotionalFile[]>([])
const beneficiaries = ref<Beneficiary[]>([])
const loading = ref(false)
const saving = ref(false)
const showDialog = ref(false)
const editingId = ref('')
const formRef = ref()

const defaultForm = { title: '', file_type: 'letter', encrypted_content: '', mime_type: '', recipient_beneficiary_id: null }
const form = reactive({ ...defaultForm })
const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
}

function fileLabel(t: string) {
  return { letter: '信件', voice: '语音', video: '视频', other: '其他' }[t] || t
}
function fileType(t: string) {
  return { letter: 'primary', voice: 'warning', video: 'danger' }[t] || 'info'
}

async function loadData() {
  try {
    const [emoRes, benRes] = await Promise.all([emotionalApi.list(), beneficiariesApi.list()])
    list.value = emoRes.data
    beneficiaries.value = benRes.data
  } catch { /* ignore */ }
}

function editItem(item: EmotionalFile) {
  editingId.value = item.id
  Object.assign(form, {
    title: item.title, file_type: item.file_type,
    encrypted_content: item.encrypted_content, mime_type: item.mime_type,
    recipient_beneficiary_id: item.recipient_beneficiary_id,
  })
  showDialog.value = true
}

async function handleSave() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  saving.value = true
  try {
    if (editingId.value) {
      await emotionalApi.update(editingId.value, form)
      ElMessage.success('更新成功')
    } else {
      await emotionalApi.create(form)
      ElMessage.success('创建成功')
    }
    showDialog.value = false
    editingId.value = ''
    Object.assign(form, defaultForm)
    await loadData()
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  } finally { saving.value = false }
}

async function handleDelete(item: EmotionalFile) {
  await ElMessageBox.confirm(`确定删除 "${item.title}" 吗？`, '确认删除')
  await emotionalApi.delete(item.id)
  ElMessage.success('删除成功')
  await loadData()
}

onMounted(loadData)
</script>

<style scoped>
.emotional-page { max-width: 1200px; }
.page-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;
}
.page-title { margin: 0; color: #303133; }
.emo-card { text-align: center; margin-bottom: 20px; }
.emo-icon { font-size: 40px; margin-bottom: 12px; }
.emo-title { font-size: 16px; font-weight: 600; color: #303133; margin-bottom: 8px; }
.emo-meta { margin-bottom: 12px; display: flex; gap: 6px; justify-content: center; }
.emo-footer { border-top: 1px solid #f0f0f0; padding-top: 12px; }
.emo-card { margin-bottom: 0; }

@media (max-width: 768px) {
  .page-header { flex-wrap: wrap; gap: 8px; }
  .page-header .el-button { width: 100%; }
}
</style>
