<template>
  <div class="vault-page">
    <!-- 页面标题 + 添加按钮 -->
    <div class="page-header">
      <h3 class="page-title">🔐 保险箱</h3>
      <el-button type="primary" @click="showDialog = true">
        <el-icon><Plus /></el-icon> 添加条目
      </el-button>
    </div>

    <!-- 分类筛选 -->
    <el-card class="filter-bar" shadow="never">
      <div class="filter-scroll">
        <el-radio-group v-model="categoryFilter" @change="loadItems">
          <el-radio-button value="">全部</el-radio-button>
          <el-radio-button value="bank">银行</el-radio-button>
          <el-radio-button value="crypto">加密货币</el-radio-button>
          <el-radio-button value="insurance">保险</el-radio-button>
          <el-radio-button value="social">社交</el-radio-button>
          <el-radio-button value="email">邮箱</el-radio-button>
          <el-radio-button value="cloud">云服务</el-radio-button>
          <el-radio-button value="instruction">关键指令</el-radio-button>
          <el-radio-button value="other">其他</el-radio-button>
        </el-radio-group>
      </div>
    </el-card>

    <!-- 条目列表 -->
    <div class="table-wrapper">
      <el-table :data="items" v-loading="loading" style="width: 100%" stripe size="small">
        <el-table-column prop="title" label="名称" min-width="140" />
        <el-table-column label="分类" width="76">
          <template #default="{ row }">
            <el-tag :type="categoryType(row.category)" size="small">{{ categoryLabel(row.category) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="platform_name" label="平台" min-width="100" />
        <el-table-column prop="account_name" label="账号" min-width="120" />
        <el-table-column label="重要" width="86">
          <template #default="{ row }">
            <el-rate v-model="row.importance" disabled :max="5" size="small" />
          </template>
        </el-table-column>
        <el-table-column label="传承" width="60">
          <template #default="{ row }">
            <el-tag :type="row.is_legacy ? 'success' : 'info'" size="small">{{ row.is_legacy ? '是' : '否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="130" fixed="right">
          <template #default="{ row }">
            <el-button text type="primary" size="small" @click="editItem(row)">编辑</el-button>
            <el-button text type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-empty v-if="!items.length && !loading" description="保险箱为空，点击右上角添加条目" />

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="showDialog" :title="editingId ? '编辑条目' : '添加条目'" width="600px" class="responsive-dialog" destroy-on-close>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="例如：工商银行储蓄卡 / 比特币钱包" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category">
            <el-option label="银行/理财" value="bank" />
            <el-option label="加密货币" value="crypto" />
            <el-option label="保险保单" value="insurance" />
            <el-option label="社交媒体" value="social" />
            <el-option label="邮箱" value="email" />
            <el-option label="云服务/网盘" value="cloud" />
            <el-option label="订阅服务" value="subscription" />
            <el-option label="关键指令" value="instruction" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="内容" prop="encrypted_content">
          <el-input v-model="form.encrypted_content" type="textarea" :rows="4"
            :placeholder="form.category === 'crypto' ? '私钥或助记词' : '账号密码等敏感信息'" />
        </el-form-item>
        <el-form-item label="平台名称">
          <el-input v-model="form.platform_name" placeholder="例如：支付宝、Google" />
        </el-form-item>
        <el-form-item label="平台网址">
          <el-input v-model="form.platform_url" placeholder="登录网址" />
        </el-form-item>
        <el-form-item label="账号">
          <el-input v-model="form.account_name" placeholder="用户名/邮箱/手机号" />
        </el-form-item>
        <el-form-item label="重要程度">
          <el-rate v-model="form.importance" :max="5" />
        </el-form-item>
        <el-form-item label="可继承">
          <el-switch v-model="form.is_legacy" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.encrypted_note" type="textarea" :rows="2" />
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
import { vaultApi, type VaultItem } from '@/api/vault'

const loading = ref(false)
const saving = ref(false)
const items = ref<VaultItem[]>([])
const showDialog = ref(false)
const editingId = ref('')
const categoryFilter = ref('')
const formRef = ref()

const defaultForm = {
  title: '', category: 'other', sub_category: '',
  encrypted_content: '', encrypted_note: '',
  platform_name: '', platform_url: '', account_name: '',
  importance: 1, is_legacy: false,
}
const form = reactive({ ...defaultForm })
const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
}

function categoryLabel(cat: string) {
  const m: Record<string, string> = {
    bank: '银行', crypto: '加密货币', insurance: '保险',
    social: '社交', email: '邮箱', cloud: '云服务',
    subscription: '订阅', instruction: '指令', other: '其他',
  }
  return m[cat] || cat
}

function categoryType(cat: string) {
  const m: Record<string, string> = {
    bank: 'success', crypto: 'danger', insurance: 'warning',
    social: 'primary', email: 'info', instruction: 'danger',
  }
  return m[cat] || 'info'
}

async function loadItems() {
  loading.value = true
  try {
    const res = await vaultApi.list(categoryFilter.value || undefined)
    items.value = res.data
  } finally { loading.value = false }
}

function editItem(row: VaultItem) {
  editingId.value = row.id
  Object.assign(form, {
    title: row.title, category: row.category, sub_category: row.sub_category,
    encrypted_content: row.encrypted_content, encrypted_note: row.encrypted_note,
    platform_name: row.platform_name, platform_url: row.platform_url,
    account_name: row.account_name, importance: row.importance, is_legacy: row.is_legacy,
  })
  showDialog.value = true
}

async function handleSave() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  saving.value = true
  try {
    if (editingId.value) {
      await vaultApi.update(editingId.value, form)
      ElMessage.success('更新成功')
    } else {
      await vaultApi.create(form)
      ElMessage.success('添加成功')
    }
    showDialog.value = false
    editingId.value = ''
    Object.assign(form, defaultForm)
    formRef.value?.resetFields()
    await loadItems()
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  } finally { saving.value = false }
}

async function handleDelete(row: VaultItem) {
  await ElMessageBox.confirm(`确定删除 "${row.title}" 吗？`, '确认删除')
  await vaultApi.delete(row.id)
  ElMessage.success('删除成功')
  await loadItems()
}

onMounted(loadItems)
</script>

<style scoped>
.vault-page { max-width: 1200px; }
.page-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;
}
.page-title { margin: 0; color: #303133; }
.filter-bar { margin-bottom: 16px; }
.filter-scroll { overflow-x: auto; white-space: nowrap; padding-bottom: 4px; }
.table-wrapper { overflow-x: auto; }

@media (max-width: 768px) {
  .page-header { flex-wrap: wrap; gap: 8px; }
  .page-header .el-button { width: 100%; }
}
@media (max-width: 640px) {
  :deep(.responsive-dialog) { width: 92% !important; max-width: 92% !important; }
  :deep(.responsive-dialog .el-dialog__body) { padding: 16px; }
}
</style>
