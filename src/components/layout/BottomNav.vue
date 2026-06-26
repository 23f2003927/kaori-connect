<template>
  <div class="k-bottom-nav k-hide-desktop">
    <router-link to="/dashboard" class="k-bottom-nav-item" id="bnav-home">
      <span class="icon">🏠</span>
      <span>Home</span>
    </router-link>
    <router-link to="/questions" class="k-bottom-nav-item" id="bnav-questions">
      <span class="icon">💭</span>
      <span>Questions</span>
    </router-link>
    <router-link to="/selfie-wall" class="k-bottom-nav-item" id="bnav-selfies">
      <span class="icon">📸</span>
      <span>Selfies</span>
    </router-link>
    <router-link to="/wardrobe" class="k-bottom-nav-item" id="bnav-wardrobe">
      <span class="icon">👗</span>
      <span>Wardrobe</span>
    </router-link>
    <router-link to="/health" class="k-bottom-nav-item" id="bnav-health">
      <span class="icon">💪</span>
      <span>Health</span>
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'BottomNav'
}
</script>
