<template>
  <el-container class="layout-container">
    <el-aside :width="isMobile ? '0' : '240px'" class="sidebar" :class="{ 'sidebar-hidden': isMobile }">
      <div class="logo">
        <el-icon :size="24"><Collection /></el-icon>
        <span>数字遗产管家</span>
      </div>
      <el-menu
        :default-active="route.path"
        router
        background-color="#2d3a4a"
        text-color="#b8c5d6"
        active-text-color="#67c23a"
      >
        <el-menu-item index="/"><el-icon><Odometer /></el-icon><span>总览面板</span></el-menu-item>
        <el-menu-item index="/vault"><el-icon><Lock /></el-icon><span>保险箱</span></el-menu-item>
        <el-menu-item index="/emotional"><el-icon><Heart /></el-icon><span>情感档案</span></el-menu-item>
        <el-menu-item index="/beneficiaries"><el-icon><UserFilled /></el-icon><span>受益人</span></el-menu-item>
        <el-menu-item index="/trigger"><el-icon><AlarmClock /></el-icon><span>生命开关</span></el-menu-item>
        <el-menu-item index="/settings"><el-icon><Setting /></el-icon><span>安全设置</span></el-menu-item>
      </el-menu>
      <div class="sidebar-footer">
        <el-button text style="color: #b8c5d6" @click="handleLogout">
          <el-icon><SwitchButton /></el-icon>
          <span style="margin-left: 8px">退出登录</span>
        </el-button>
      </div>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-button v-if="isMobile" text class="menu-btn" @click="drawerVisible = true">
            <el-icon :size="22"><Expand /></el-icon>
          </el-button>
          <span class="welcome">🌱 你好，{{ auth.displayName }}</span>
        </div>
        <div class="header-right">
          <el-button type="success" size="small" round @click="$router.push('/trigger')">
            <el-icon><Select /></el-icon>
            <span class="checkin-text">安全打卡</span>
          </el-button>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>

    <el-drawer
      v-model="drawerVisible"
      direction="ltr"
      size="260px"
      :with-header="false"
      :show-close="false"
    >
      <div class="drawer-menu">
        <div class="drawer-logo">
          <el-icon :size="24"><Collection /></el-icon>
          <span>数字遗产管家</span>
        </div>
        <el-menu
          :default-active="route.path"
          router
          @select="drawerVisible = false"
        >
          <el-menu-item index="/"><el-icon><Odometer /></el-icon><span>总览面板</span></el-menu-item>
          <el-menu-item index="/vault"><el-icon><Lock /></el-icon><span>保险箱</span></el-menu-item>
          <el-menu-item index="/emotional"><el-icon><Heart /></el-icon><span>情感档案</span></el-menu-item>
          <el-menu-item index="/beneficiaries"><el-icon><UserFilled /></el-icon><span>受益人</span></el-menu-item>
          <el-menu-item index="/trigger"><el-icon><AlarmClock /></el-icon><span>生命开关</span></el-menu-item>
          <el-menu-item index="/settings"><el-icon><Setting /></el-icon><span>安全设置</span></el-menu-item>
        </el-menu>
        <div class="drawer-footer">
          <el-button text style="color: #606266; width: 100%; justify-content: flex-start;" @click="handleLogout">
            <el-icon><SwitchButton /></el-icon>
            <span style="margin-left: 8px">退出登录</span>
          </el-button>
        </div>
      </div>
    </el-drawer>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const drawerVisible = ref(false)
const isMobile = ref(false)

function checkMobile() {
  isMobile.value = window.innerWidth < 768
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})
onUnmounted(() => window.removeEventListener('resize', checkMobile))
</script>

<style scoped>
.layout-container { height: 100vh; }
.sidebar {
  background-color: #2d3a4a;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
  overflow: hidden;
}
.sidebar-hidden { width: 0 !important; overflow: hidden; }
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  color: #e8f0fe;
  font-size: 18px;
  font-weight: 600;
  gap: 10px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  white-space: nowrap;
}
.el-menu { border-right: none; flex: 1; }
.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid rgba(255,255,255,0.06);
}
.header {
  background: #fff;
  border-bottom: 1px solid #e8edf2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  height: 56px;
}
.header-left { display: flex; align-items: center; gap: 8px; }
.menu-btn { color: #5a6a7a; }
.welcome { color: #5a6a7a; font-size: 14px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px; }
.main-content {
  background-color: #f0f4f8;
  padding: 16px;
  min-height: calc(100vh - 56px);
}

.drawer-menu { height: 100%; display: flex; flex-direction: column; }
.drawer-logo {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  font-size: 18px;
  font-weight: 600;
  gap: 10px;
  color: #303133;
  border-bottom: 1px solid #e8edf2;
}
.drawer-footer {
  padding: 16px 20px;
  border-top: 1px solid #e8edf2;
}

@media (max-width: 768px) {
  .main-content { padding: 12px; }
  .welcome { max-width: 100px; font-size: 13px; }
  .checkin-text { display: none; }
}
</style>
