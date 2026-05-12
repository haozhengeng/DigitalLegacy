<template>
  <el-container class="layout-container">
    <el-aside width="240px" class="sidebar">
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
        <el-menu-item index="/">
          <el-icon><Odometer /></el-icon>
          <span>总览面板</span>
        </el-menu-item>
        <el-menu-item index="/vault">
          <el-icon><Lock /></el-icon>
          <span>保险箱</span>
        </el-menu-item>
        <el-menu-item index="/emotional">
          <el-icon><Heart /></el-icon>
          <span>情感档案</span>
        </el-menu-item>
        <el-menu-item index="/beneficiaries">
          <el-icon><UserFilled /></el-icon>
          <span>受益人</span>
        </el-menu-item>
        <el-menu-item index="/trigger">
          <el-icon><AlarmClock /></el-icon>
          <span>生命开关</span>
        </el-menu-item>
        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <span>安全设置</span>
        </el-menu-item>
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
          <span class="welcome">🌱 你好，{{ auth.displayName }}</span>
        </div>
        <div class="header-right">
          <el-button type="success" size="small" round @click="$router.push('/trigger')">
            <el-icon><Select /></el-icon> 安全打卡
          </el-button>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout-container { height: 100vh; }
.sidebar {
  background-color: #2d3a4a;
  display: flex;
  flex-direction: column;
}
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
  padding: 0 24px;
  height: 56px;
}
.welcome { color: #5a6a7a; font-size: 15px; font-weight: 500; }
.main-content {
  background-color: #f0f4f8;
  padding: 24px;
  min-height: calc(100vh - 56px);
}
</style>
