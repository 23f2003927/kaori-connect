<template>
  <div class="container py-4">
    <!-- Welcome Header -->
    <div class="k-page-header">
      <h1>Welcome back, {{ userName }} 💕</h1>
      <p>Here's what's happening in your Kaori space today</p>
    </div>

    <!-- Dashboard Grid -->
    <div class="k-grid k-grid-2 mb-4">
      <!-- Today's Question Card -->
      <div class="k-card k-dash-card" id="dash-question">
        <div class="k-dash-card-header">
          <h3>💭 Today's Question</h3>
          <span class="k-badge k-badge-lavender">{{ todayQuestion.category || 'Random' }}</span>
        </div>
        <p style="font-size:1.05rem; font-weight:600; margin-bottom:1rem;">
          {{ todayQuestion.text || "What made you fall in love with me?" }}
        </p>
        <router-link to="/questions" class="k-btn k-btn-soft" id="dash-answer-btn">
          Answer Now ✨
        </router-link>
      </div>

      <!-- Passive Updates Card -->
      <div class="k-card k-dash-card" id="dash-activity">
        <div class="k-dash-card-header">
          <h3>📋 Recent Activity</h3>
          <span class="k-badge k-badge-mint">Live</span>
        </div>
        <div v-if="activities.length">
          <div v-for="act in activities.slice(0, 4)" :key="act.id" class="d-flex align-items-start gap-2 mb-2" style="font-size:0.9rem;">
            <span>{{ act.icon }}</span>
            <div>
              <span style="font-weight:600;">{{ act.user }}</span>
              {{ act.text }}
              <div style="font-size:0.75rem; color:var(--k-text-muted);">{{ act.time }}</div>
            </div>
          </div>
        </div>
        <div v-else class="k-empty" style="padding:1rem;">
          <p>No activity yet today. Start something! 🌟</p>
        </div>
      </div>

      <!-- Health Progress Card -->
      <div class="k-card k-dash-card" id="dash-health">
        <div class="k-dash-card-header">
          <h3>💪 Health Progress</h3>
          <span class="k-streak" v-if="streak > 0">🔥 {{ streak }} day streak</span>
        </div>
        <div v-for="goal in healthGoals.slice(0, 3)" :key="goal.id" class="mb-3">
          <div class="d-flex justify-content-between mb-1" style="font-size:0.85rem;">
            <span style="font-weight:600;">{{ goal.icon }} {{ goal.name }}</span>
            <span class="k-badge" :class="statusBadge(goal.status)">{{ goal.status }}</span>
          </div>
          <div class="k-progress">
            <div class="k-progress-bar" :style="{ width: goal.progress + '%' }"></div>
          </div>
        </div>
        <router-link to="/health" class="k-btn k-btn-soft mt-2" id="dash-health-btn" style="font-size:0.85rem;">
          View All Goals →
        </router-link>
      </div>

      <!-- Random Selfie Card -->
      <div class="k-card k-dash-card" id="dash-selfie">
        <div class="k-dash-card-header">
          <h3>📸 Random Memory</h3>
          <button class="k-btn k-btn-soft" @click="shuffleSelfie" id="dash-shuffle-selfie" style="font-size:0.8rem; padding:0.3rem 0.8rem;">
            🔀 Shuffle
          </button>
        </div>
        <div v-if="randomSelfie" class="k-image-card" style="aspect-ratio:4/3; border-radius:var(--k-radius-sm);">
          <img :src="randomSelfie.url" :alt="randomSelfie.caption || 'Memory'" />
          <div class="k-image-overlay">
            <p style="margin:0; font-size:0.85rem;">{{ randomSelfie.caption || '💕' }}</p>
          </div>
        </div>
        <div v-else class="k-empty" style="padding:2rem 1rem;">
          <div class="k-empty-icon">📷</div>
          <p>No selfies yet! Upload your first one.</p>
          <router-link to="/selfie-wall" class="k-btn k-btn-soft" style="font-size:0.85rem;">Upload Selfie</router-link>
        </div>
      </div>

      <!-- Wardrobe Requests Card -->
      <div class="k-card k-dash-card" id="dash-wardrobe">
        <div class="k-dash-card-header">
          <h3>👗 Wardrobe Requests</h3>
          <span class="k-badge k-badge-peach" v-if="wardrobeRequests.length">{{ wardrobeRequests.length }} pending</span>
        </div>
        <div v-if="wardrobeRequests.length">
          <div v-for="req in wardrobeRequests.slice(0, 3)" :key="req.id" class="d-flex align-items-center gap-2 mb-2 p-2" style="background:var(--k-cream); border-radius:var(--k-radius-sm);">
            <span style="font-size:1.5rem;">👕</span>
            <div style="flex:1;">
              <div style="font-weight:600; font-size:0.85rem;">{{ req.message }}</div>
              <div style="font-size:0.75rem; color:var(--k-text-muted);">From {{ req.from }}</div>
            </div>
            <span class="k-badge k-badge-pink">{{ req.status }}</span>
          </div>
        </div>
        <div v-else class="k-empty" style="padding:1rem;">
          <p>No wardrobe requests 👗</p>
        </div>
        <router-link to="/wardrobe" class="k-btn k-btn-soft mt-2" id="dash-wardrobe-btn" style="font-size:0.85rem;">
          Open Wardrobe →
        </router-link>
      </div>

      <!-- Couple Games Card -->
      <div class="k-card k-dash-card" id="dash-games">
        <div class="k-dash-card-header">
          <h3>🎮 Couple Games</h3>
        </div>
        <div class="d-flex flex-wrap gap-2">
          <div v-for="game in games" :key="game.name" class="text-center p-2" style="background:var(--k-cream); border-radius:var(--k-radius-sm); flex:1; min-width:100px; cursor:pointer;" @click="playGame(game)">
            <div style="font-size:2rem;">{{ game.icon }}</div>
            <div style="font-size:0.8rem; font-weight:600;">{{ game.name }}</div>
          </div>
        </div>
      </div>

      <!-- Widgets Preview Card -->
      <div class="k-card k-dash-card" id="dash-widgets">
        <div class="k-dash-card-header">
          <h3>🎨 Widgets</h3>
          <span class="k-badge k-badge-lavender">Customizable</span>
        </div>
        <div class="row g-2">
          <!-- Love Meter -->
          <div class="col-6">
            <div class="text-center p-2" style="background:var(--k-cream); border-radius:var(--k-radius-sm);">
              <div style="font-size:1.5rem;" class="k-heartbeat">💕</div>
              <div style="font-size:0.8rem; font-weight:600;">Love Meter</div>
              <div style="font-size:1.2rem; font-weight:800; color:var(--k-pink-dark);">98%</div>
            </div>
          </div>
          <!-- Mood -->
          <div class="col-6">
            <div class="text-center p-2" style="background:var(--k-cream); border-radius:var(--k-radius-sm);">
              <div style="font-size:1.5rem;">😊</div>
              <div style="font-size:0.8rem; font-weight:600;">Today's Mood</div>
              <div style="font-size:0.75rem; color:var(--k-text-light);">Happy & cozy</div>
            </div>
          </div>
          <!-- Quote -->
          <div class="col-12">
            <div class="text-center p-2" style="background:var(--k-cream); border-radius:var(--k-radius-sm);">
              <div style="font-size:0.85rem; font-style:italic; color:var(--k-text-light);">
                "The best thing to hold onto in life is each other." — Audrey Hepburn
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Relationship Stats Card -->
      <div class="k-card k-dash-card" id="dash-stats">
        <div class="k-dash-card-header">
          <h3>📊 Relationship Stats</h3>
        </div>
        <div class="row g-2 text-center">
          <div class="col-4">
            <div style="font-size:1.8rem; font-weight:800; color:var(--k-pink-dark);">{{ stats.daysTogether }}</div>
            <div style="font-size:0.75rem; color:var(--k-text-light);">Days Together</div>
          </div>
          <div class="col-4">
            <div style="font-size:1.8rem; font-weight:800; color:var(--k-lavender-dark);">{{ stats.questionsAnswered }}</div>
            <div style="font-size:0.75rem; color:var(--k-text-light);">Questions</div>
          </div>
          <div class="col-4">
            <div style="font-size:1.8rem; font-weight:800; color:var(--k-pink-dark);">{{ stats.selfiesShared }}</div>
            <div style="font-size:0.75rem; color:var(--k-text-light);">Selfies</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, inject, onMounted } from 'vue'
import { supabase } from '@/services/supabase.js'

export default {
  name: 'DashboardPage',
  setup() {
    const user = inject('user')
    const userName = ref('Love')
    const todayQuestion = ref({ text: "What's one thing about me that always makes you smile?", category: 'Romantic' })
    const activities = ref([])
    const healthGoals = ref([
      { id: 1, name: 'Running', icon: '🏃', status: 'In Progress', progress: 65 },
      { id: 2, name: 'Water Intake', icon: '💧', status: 'Completed', progress: 100 },
      { id: 3, name: 'Yoga', icon: '🧘', status: 'Not Started', progress: 0 },
    ])
    const streak = ref(5)
    const randomSelfie = ref(null)
    const wardrobeRequests = ref([])
    const games = [
      { name: 'Trivia', icon: '🧠' },
      { name: 'Would You Rather', icon: '🤔' },
      { name: 'Truth or Dare', icon: '🎯' },
    ]
    const stats = ref({ daysTogether: 142, questionsAnswered: 38, selfiesShared: 24 })

    onMounted(async () => {
      // Load user name
      if (user.value) {
        const { data } = await supabase.from('profiles').select('display_name').eq('id', user.value.id).single()
        if (data) userName.value = data.display_name || 'Love'
      }

      // Load activity feed
      try {
        const { data } = await supabase
          .from('activity_feed')
          .select('*')
          .order('created_at', { ascending: false })
          .limit(4)
        if (data) activities.value = data.map(a => ({
          id: a.id,
          icon: a.icon || '💕',
          user: a.user_name || 'Partner',
          text: a.text || a.action,
          time: timeAgo(a.created_at)
        }))
      } catch (e) { /* tables may not exist yet */ }

      // Load random selfie
      try {
        const { data } = await supabase.from('selfies').select('*').limit(10)
        if (data?.length) {
          const rand = data[Math.floor(Math.random() * data.length)]
          randomSelfie.value = { url: rand.image_url, caption: rand.caption }
        }
      } catch (e) { /* ok */ }

      // Load wardrobe requests
      try {
        const { data } = await supabase
          .from('wardrobe_requests')
          .select('*')
          .eq('status', 'Pending')
          .limit(3)
        if (data) wardrobeRequests.value = data.map(r => ({
          id: r.id,
          message: r.message || 'Wear request',
          from: r.from_name || 'Partner',
          status: r.status
        }))
      } catch (e) { /* ok */ }

      // Load stats
      try {
        const { data } = await supabase.from('relationship_stats').select('*').limit(1).single()
        if (data) stats.value = data
      } catch (e) { /* ok, use defaults */ }
    })

    function shuffleSelfie() {
      // Re-fetch random selfie
      supabase.from('selfies').select('*').limit(10).then(({ data }) => {
        if (data?.length) {
          const rand = data[Math.floor(Math.random() * data.length)]
          randomSelfie.value = { url: rand.image_url, caption: rand.caption }
        }
      })
    }

    function playGame(game) {
      // placeholder
    }

    function statusBadge(status) {
      if (status === 'Completed') return 'k-badge-mint'
      if (status === 'In Progress') return 'k-badge-peach'
      return 'k-badge-lavender'
    }

    function timeAgo(date) {
      if (!date) return 'just now'
      const mins = Math.floor((Date.now() - new Date(date)) / 60000)
      if (mins < 1) return 'just now'
      if (mins < 60) return `${mins}m ago`
      const hours = Math.floor(mins / 60)
      if (hours < 24) return `${hours}h ago`
      return `${Math.floor(hours / 24)}d ago`
    }

    return {
      userName, todayQuestion, activities, healthGoals, streak,
      randomSelfie, wardrobeRequests, games, stats,
      shuffleSelfie, playGame, statusBadge
    }
  }
}
</script>
