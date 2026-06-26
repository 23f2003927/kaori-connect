<template>
  <nav class="k-navbar">
    <div class="container">
      <div class="d-flex align-items-center justify-content-between">
        <!-- Brand -->
        <router-link to="/dashboard" class="navbar-brand d-flex align-items-center gap-2 text-decoration-none">
          <span style="font-size:1.4rem">💕</span>
          <span>Kaori</span>
        </router-link>

        <!-- Desktop Nav -->
        <div class="d-none d-md-flex align-items-center gap-1">
          <router-link to="/dashboard" class="k-nav-link" id="nav-dashboard">🏠 Home</router-link>
          <router-link to="/questions" class="k-nav-link" id="nav-questions">💭 Questions</router-link>
          <router-link to="/selfie-wall" class="k-nav-link" id="nav-selfies">📸 Selfies</router-link>
          <router-link to="/wardrobe" class="k-nav-link" id="nav-wardrobe">👗 Wardrobe</router-link>
          <router-link to="/health" class="k-nav-link" id="nav-health">💪 Health</router-link>
        </div>

        <!-- Right side -->
        <div class="d-flex align-items-center gap-2">
          <router-link to="/notifications" class="k-btn-icon k-btn-soft k-notif-dot" id="nav-notifications" title="Notifications">
            🔔
          </router-link>
          <button class="k-theme-toggle" @click="$emit('toggle-theme')" id="theme-toggle" :title="theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'">
            {{ theme === 'light' ? '🌙' : '☀️' }}
          </button>
          <router-link to="/profile" class="k-btn-icon k-btn-soft" id="nav-profile" title="Profile">
            👤
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  props: {
    theme: { type: String, default: 'light' }
  },
  emits: ['toggle-theme']
}
</script>
