<template>
  <div class="beneficiaries-page">
    <div class="page-header">
      <h3 class="page-title">👨‍👩‍👧 受益人</h3>
      <el-button type="primary" @click="showDialog = true">
        <el-icon><Plus /></el-icon> 邀请受益人
      </el-button>
    </div>

    <el-row :gutter="20">
      <el-col :span="8" v-for="b in list" :key="b.id">
        <el-card shadow="hover" class="ben-card">
          <div class="card-header">
            <el-avatar :size="48" class="avatar">{{ b.name.charAt(0) }}</el-avatar>
            <div>
              <div class="ben-name">{{ b.name }}</div>
              <div class="ben-relation">{{ b.relation || '未设置关系' }}</div>
            </div>
          </div>
          <div class="card-body">
            <div class="info-row"><el-icon><Message /></el-icon> {{ b.email }}</div>
            <div class="info-row" v-if="b.phone"><el-icon><Phone /></el-icon> {{ b.phone }}</div>
            <div class="permissions">
              <el-tag v-if="b.permission_vault" size="small" type="primary">保险箱</el-tag>
              <el-tag v-if="b.permission_emotional" size="small" type="warning">情感档案</el-tag>
              <el-tag v-if="b.permission_key_fragments" size="small" type="danger">密钥分片</el-tag>
              <span v-if="!b.permission_vault && !b.permission_emotional && !b.permission_key_fragments" class="no-perm">无查看权限</span>
            </div>
          </div>
          <div class="card-footer">
            <el-tag :type="b.is_identity_verified ? 'success' : 'info'" size="small">
              {{ b.is_identity_verified ? '已验证' : '未认证' }}
            </el-tag>
            <div>
              <el-button text type="primary" size="small" @click="editItem(b)">编辑</el-button>
              <el-button text type="danger" size="small" @click="handleDelete(b)">删除</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-empty v-if="!list.length" description="暂无受益人，邀请信任的人作为您的数字遗产继承人" />

    <el-dialog v-model="showDialog" :title="editingId ? '编辑受益人' : '邀请受益人'" width="550px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="关系">
          <el-select v-model="form.relation" placeholder="选择关系">
            <el-option label="配偶" value="配偶" />
            <el-option label="子女" value="子女" />
            <el-option label="父母" value="父母" />
            <el-option label="兄弟姐妹" value="兄弟姐妹" />
            <el-option label="好友" value="好友" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="查看权限">
          <el-checkbox v-model="form.permission_vault">保险箱</el-checkbox>
          <el-checkbox v-model="form.permission_emotional">情感档案</el-checkbox>
          <el-checkbox v-model="form.permission_key_fragments">密钥分片</el-checkbox>
          <div class="perm-hint">触发后受益人可查看授权的内容</div>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.notes" type="textarea" :rows="2" />
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
import { beneficiariesApi, type Beneficiary } from '@/api/beneficiaries'

const list = ref<Beneficiary[]>([])
const loading = ref(false)
const saving = ref(false)
const showDialog = ref(false)
const editingId = ref('')
const formRef = ref()

const defaultForm = {
  name: '', email: '', phone: '', relation: '',
  permission_vault: false, permission_emotional: false,
  permission_key_fragments: false, notes: '',
}
const form = reactive({ ...defaultForm })
const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
}

async function loadList() {
  loading.value = true
  try {
    const res = await beneficiariesApi.list()
    list.value = res.data
  } finally { loading.value = false }
}

function editItem(item: Beneficiary) {
  editingId.value = item.id
  Object.assign(form, {
    name: item.name, email: item.email, phone: item.phone, relation: item.relation,
    permission_vault: item.permission_vault, permission_emotional: item.permission_emotional,
    permission_key_fragments: item.permission_key_fragments, notes: item.notes,
  })
  showDialog.value = true
}

async function handleSave() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  saving.value = true
  try {
    if (editingId.value) {
      await beneficiariesApi.update(editingId.value, form)
      ElMessage.success('更新成功')
    } else {
      await beneficiariesApi.create(form)
      ElMessage.success('邀请成功')
    }
    showDialog.value = false
    editingId.value = ''
    Object.assign(form, defaultForm)
    await loadList()
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  } finally { saving.value = false }
}

async function handleDelete(item: Beneficiary) {
  await ElMessageBox.confirm(`确定移除受益人 "${item.name}" 吗？`, '确认删除')
  await beneficiariesApi.delete(item.id)
  ElMessage.success('已移除')
  await loadList()
}

onMounted(loadList)
</script>

<style scoped>
.beneficiaries-page { max-width: 1200px; }
.page-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;
}
.page-title { margin: 0; color: #303133; }
.ben-card { margin-bottom: 20px; }
.card-header { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; }
.avatar { background: #409eff; color: #fff; }
.ben-name { font-size: 16px; font-weight: 600; color: #303133; }
.ben-relation { font-size: 13px; color: #909399; margin-top: 2px; }
.card-body { margin-bottom: 14px; }
.info-row { display: flex; align-items: center; gap: 6px; color: #606266; font-size: 13px; margin-bottom: 6px; }
.permissions { margin-top: 10px; display: flex; gap: 4px; flex-wrap: wrap; }
.no-perm { color: #c0c4cc; font-size: 12px; }
.card-footer {
  display: flex; justify-content: space-between; align-items: center;
  padding-top: 12px; border-top: 1px solid #f0f0f0;
}
.perm-hint { color: #909399; font-size: 12px; margin-top: 4px; }
</style>
