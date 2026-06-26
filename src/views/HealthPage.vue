<template>
  <div class="container py-4">
    <div class="k-page-header">
      <h1>💪 Health Planner</h1>
      <p>Track your goals and cheer each other on</p>
    </div>

    <!-- Tabs -->
    <div class="k-pills justify-content-center mb-4">
      <button class="k-pill" :class="{ active: tab === 'mine' }" @click="tab = 'mine'">🏃 My Goals</button>
      <button class="k-pill" :class="{ active: tab === 'partner' }" @click="tab = 'partner'">💕 Partner's Goals</button>
    </div>

    <!-- Add Goal Button -->
    <div class="text-center mb-4" v-if="tab === 'mine'">
      <button class="k-btn k-btn-primary" @click="showAddGoal = true" id="add-goal-btn">
        ➕ Add Health Goal
      </button>
    </div>

    <!-- Add Goal Modal -->
    <div v-if="showAddGoal" class="k-modal-backdrop" @click.self="showAddGoal = false">
      <div class="k-modal">
        <div class="k-modal-header">
          <h3>🎯 New Health Goal</h3>
          <button class="k-modal-close" @click="showAddGoal = false">&times;</button>
        </div>
        <div class="k-form-group">
          <label class="k-label">Activity Type</label>
          <div class="k-pills flex-wrap">
            <button v-for="type in goalTypes" :key="type.name" class="k-pill" :class="{ active: newGoal.type === type.name }" @click="newGoal.type = type.name">
              {{ type.icon }} {{ type.name }}
            </button>
          </div>
        </div>
        <div class="k-form-group">
          <label class="k-label" for="goal-target">Daily Target (optional)</label>
          <input class="k-input" id="goal-target" v-model="newGoal.target" placeholder="e.g., 30 minutes, 8 glasses" />
        </div>
        <button class="k-btn k-btn-primary w-100 justify-content-center" @click="createGoal" :disabled="!newGoal.type" id="save-goal-btn">
          Create Goal ✨
        </button>
      </div>
    </div>

    <!-- Goals List -->
    <div class="k-grid k-grid-2">
      <div v-for="goal in displayGoals" :key="goal.id" class="k-card k-dash-card">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <div>
            <h4 style="font-size:1.1rem; margin:0;">
              {{ goalIcon(goal.type) }} {{ goal.type }}
            </h4>
            <span style="font-size:0.8rem; color:var(--k-text-muted);">{{ goal.target || 'Daily' }}</span>
          </div>
          <div class="d-flex align-items-center gap-2">
            <span class="k-streak" v-if="goal.streak > 0">🔥 {{ goal.streak }}</span>
            <span class="k-badge" :class="statusBadge(goal.status)">{{ goal.status }}</span>
          </div>
        </div>

        <div class="k-progress mb-2">
          <div class="k-progress-bar" :style="{ width: statusProgress(goal.status) + '%' }"></div>
        </div>

        <!-- Status controls (my goals only) -->
        <div v-if="tab === 'mine'" class="d-flex gap-2 flex-wrap mb-2">
          <button v-for="s in ['Not Started', 'In Progress', 'Completed']" :key="s" class="k-pill" :class="{ active: goal.status === s }" @click="updateStatus(goal, s)" style="font-size:0.75rem; padding:0.3rem 0.7rem;">
            {{ statusEmoji(s) }} {{ s }}
          </button>
        </div>

        <!-- Reactions (partner goals only) -->
        <div v-if="tab === 'partner'" class="k-reactions">
          <button class="k-reaction" @click="reactToGoal(goal, '❤️')" title="Cheer">❤️ Cheer</button>
          <button class="k-reaction" @click="reactToGoal(goal, '🔥')" title="Keep Going">🔥 Keep Going</button>
          <button class="k-reaction" @click="reactToGoal(goal, '🎉')" title="Congrats">🎉 Congrats</button>
        </div>

        <!-- Recent log -->
        <div v-if="goal.lastLog" style="font-size:0.75rem; color:var(--k-text-muted); margin-top:0.5rem;">
          Last updated: {{ formatDate(goal.lastLog) }}
        </div>
      </div>
    </div>

    <div v-if="!displayGoals.length" class="k-empty">
      <div class="k-empty-icon">💪</div>
      <p>{{ tab === 'mine' ? 'No health goals yet. Create one above!' : "Your partner hasn't set any goals yet." }}</p>
    </div>

    <!-- Streak Stats -->
    <div v-if="tab === 'mine' && myGoals.length" class="k-card mt-4" style="text-align:center;">
      <h3 style="font-size:1.1rem; margin-bottom:1rem;">📊 Your Streak Stats</h3>
      <div class="row g-3">
        <div class="col-4">
          <div style="font-size:2rem; font-weight:800; color:var(--k-pink-dark);">{{ totalStreak }}</div>
          <div style="font-size:0.8rem; color:var(--k-text-light);">Best Streak</div>
        </div>
        <div class="col-4">
          <div style="font-size:2rem; font-weight:800; color:var(--k-lavender-dark);">{{ completedToday }}</div>
          <div style="font-size:0.8rem; color:var(--k-text-light);">Done Today</div>
        </div>
        <div class="col-4">
          <div style="font-size:2rem; font-weight:800; color:var(--k-pink-dark);">{{ myGoals.length }}</div>
          <div style="font-size:0.8rem; color:var(--k-text-light);">Active Goals</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, inject, onMounted } from 'vue'
import { supabase } from '@/services/supabase.js'

export default {
  name: 'HealthPage',
  setup() {
    const showToast = inject('showToast')
    const user = inject('user')
    const tab = ref('mine')
    const myGoals = ref([])
    const partnerGoals = ref([])
    const showAddGoal = ref(false)
    const newGoal = ref({ type: '', target: '' })

    const goalTypes = [
      { name: 'Running', icon: '🏃' },
      { name: 'Gym', icon: '🏋️' },
      { name: 'Yoga', icon: '🧘' },
      { name: 'Water Intake', icon: '💧' },
      { name: 'Reading', icon: '📚' },
      { name: 'Meditation', icon: '🧠' },
      { name: 'Sleep', icon: '😴' },
    ]

    const displayGoals = computed(() => tab.value === 'partner' ? partnerGoals.value : myGoals.value)
    const totalStreak = computed(() => Math.max(0, ...myGoals.value.map(g => g.streak || 0)))
    const completedToday = computed(() => myGoals.value.filter(g => g.status === 'Completed').length)

    onMounted(loadGoals)

    async function loadGoals() {
      try {
        const { data } = await supabase.from('health_plans').select('*').eq('user_id', user.value?.id).order('created_at', { ascending: false })
        if (data) myGoals.value = data
      } catch (e) { /* ok */ }

      try {
        const { data: profile } = await supabase.from('profiles').select('partner_id').eq('id', user.value?.id).single()
        if (profile?.partner_id) {
          const { data } = await supabase.from('health_plans').select('*').eq('user_id', profile.partner_id)
          if (data) partnerGoals.value = data
        }
      } catch (e) { /* ok */ }
    }

    async function createGoal() {
      try {
        await supabase.from('health_plans').insert({
          user_id: user.value.id,
          type: newGoal.value.type,
          target: newGoal.value.target || null,
          status: 'Not Started',
          streak: 0,
          created_at: new Date().toISOString()
        })
        showToast('Goal created! 💪')
        showAddGoal.value = false
        newGoal.value = { type: '', target: '' }
        await loadGoals()
      } catch (e) {
        showToast('Failed to create goal')
      }
    }

    async function updateStatus(goal, status) {
      try {
        const updates = { status }
        if (status === 'Completed') {
          updates.streak = (goal.streak || 0) + 1
          updates.last_completed = new Date().toISOString()

          // Log activity
          const icon = status === 'Completed' ? '✅' : '🏃'
          const text = status === 'Completed' ? `Completed ${goal.type}` : `Started ${goal.type}`
          await supabase.from('activity_feed').insert({
            user_id: user.value.id, action: 'health_update', icon, text,
            created_at: new Date().toISOString()
          })
        }
        await supabase.from('health_plans').update(updates).eq('id', goal.id)
        goal.status = status
        if (updates.streak) goal.streak = updates.streak
        showToast(`${goal.type}: ${status}`)
      } catch (e) { /* ok */ }
    }

    async function reactToGoal(goal, emoji) {
      showToast(`${emoji} Sent to your partner!`)
      try {
        await supabase.from('notifications').insert({
          user_id: goal.user_id,
          type: 'health_reaction',
          message: `Your partner reacted ${emoji} to your ${goal.type} goal!`,
          created_at: new Date().toISOString()
        })
      } catch (e) { /* ok */ }
    }

    function goalIcon(type) {
      return goalTypes.find(g => g.name === type)?.icon || '🎯'
    }
    function statusBadge(s) {
      if (s === 'Completed') return 'k-badge-mint'
      if (s === 'In Progress') return 'k-badge-peach'
      return 'k-badge-lavender'
    }
    function statusProgress(s) {
      if (s === 'Completed') return 100
      if (s === 'In Progress') return 50
      return 0
    }
    function statusEmoji(s) {
      if (s === 'Completed') return '✅'
      if (s === 'In Progress') return '🏃'
      return '⏸️'
    }
    function formatDate(d) {
      if (!d) return ''
      return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }

    return {
      tab, myGoals, partnerGoals, displayGoals, showAddGoal, newGoal,
      goalTypes, totalStreak, completedToday,
      createGoal, updateStatus, reactToGoal, goalIcon, statusBadge,
      statusProgress, statusEmoji, formatDate
    }
  }
}
</script>
