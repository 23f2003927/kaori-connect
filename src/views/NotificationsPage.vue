<template>
  <div class="container py-4">
    <div class="k-page-header">
      <h1>🔔 Notifications</h1>
      <p>Stay updated with your Kaori space</p>
    </div>

    <div class="text-end mb-3" v-if="notifications.length">
      <button class="k-btn k-btn-soft" @click="markAllRead" id="mark-all-read" style="font-size:0.85rem;">
        ✅ Mark all read
      </button>
    </div>

    <div class="row justify-content-center">
      <div class="col-lg-7">
        <div v-for="notif in notifications" :key="notif.id" class="k-card mb-3 d-flex align-items-start gap-3" :style="{ opacity: notif.read ? 0.6 : 1 }">
          <div style="font-size:1.5rem; flex-shrink:0;">{{ notifIcon(notif.type) }}</div>
          <div style="flex:1;">
            <p style="margin:0; font-weight:600; font-size:0.95rem;">{{ notif.message }}</p>
            <span style="font-size:0.75rem; color:var(--k-text-muted);">{{ timeAgo(notif.created_at) }}</span>
          </div>
          <button v-if="!notif.read" class="k-btn-icon k-btn-soft" @click="markRead(notif)" style="font-size:0.8rem; width:32px; height:32px;">
            ✓
          </button>
        </div>

        <div v-if="!notifications.length" class="k-empty">
          <div class="k-empty-icon">🔔</div>
          <p>No notifications yet. Your partner actions will appear here!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, inject, onMounted } from 'vue'
import { supabase } from '@/services/supabase.js'

export default {
  name: 'NotificationsPage',
  setup() {
    const user = inject('user')
    const notifications = ref([])

    onMounted(async () => {
      try {
        const { data } = await supabase
          .from('notifications')
          .select('*')
          .eq('user_id', user.value?.id)
          .order('created_at', { ascending: false })
          .limit(30)
        if (data) notifications.value = data
      } catch (e) { /* ok */ }
    })

    async function markRead(notif) {
      try {
        await supabase.from('notifications').update({ read: true }).eq('id', notif.id)
        notif.read = true
      } catch (e) { /* ok */ }
    }

    async function markAllRead() {
      try {
        await supabase.from('notifications').update({ read: true }).eq('user_id', user.value?.id)
        notifications.value.forEach(n => n.read = true)
      } catch (e) { /* ok */ }
    }

    function notifIcon(type) {
      const icons = { question: '💭', selfie: '📸', wardrobe: '👕', health: '💪', health_reaction: '❤️', general: '💕' }
      return icons[type] || '💕'
    }

    function timeAgo(date) {
      if (!date) return ''
      const mins = Math.floor((Date.now() - new Date(date)) / 60000)
      if (mins < 1) return 'just now'
      if (mins < 60) return `${mins}m ago`
      const hours = Math.floor(mins / 60)
      if (hours < 24) return `${hours}h ago`
      return `${Math.floor(hours / 24)}d ago`
    }

    return { notifications, markRead, markAllRead, notifIcon, timeAgo }
  }
}
</script>
