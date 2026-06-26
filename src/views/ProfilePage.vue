<template>
  <div class="container py-4">
    <div class="k-page-header">
      <h1>👤 Profile</h1>
      <p>Manage your account and settings</p>
    </div>

    <div class="row justify-content-center">
      <div class="col-lg-6">
        <!-- Profile Card -->
        <div class="k-card mb-4 text-center">
          <div class="mb-3" style="font-size:4rem;">💕</div>
          <h2 style="font-size:1.5rem;">{{ profile.display_name }}</h2>
          <p style="color:var(--k-text-light);">{{ profile.email }}</p>

          <!-- Partner Code -->
          <div class="k-card mb-3" style="background:var(--k-cream);">
            <p style="font-size:0.8rem; color:var(--k-text-muted); margin-bottom:0.3rem;">Your Partner Code</p>
            <div style="font-size:1.5rem; font-weight:800; letter-spacing:3px; color:var(--k-pink-dark);">
              {{ profile.partner_code || '...' }}
            </div>
          </div>

          <!-- Partner Info -->
          <div v-if="partner" class="k-card" style="background:var(--k-lavender-light);">
            <p style="font-size:0.8rem; color:var(--k-lavender-dark); margin-bottom:0.3rem;">Linked Partner</p>
            <h4 style="margin:0; color:var(--k-lavender-dark);">💕 {{ partner.display_name }}</h4>
          </div>
          <div v-else>
            <router-link to="/link-partner" class="k-btn k-btn-primary">🔗 Link Partner</router-link>
          </div>
        </div>

        <!-- Edit Profile -->
        <div class="k-card mb-4">
          <h3 style="font-size:1.1rem; margin-bottom:1rem;">✏️ Edit Profile</h3>
          <div class="k-form-group">
            <label class="k-label" for="edit-name">Display Name</label>
            <input class="k-input" id="edit-name" v-model="editName" />
          </div>
          <button class="k-btn k-btn-primary" @click="updateProfile" :disabled="saving" id="save-profile-btn">
            {{ saving ? 'Saving...' : 'Save Changes ✨' }}
          </button>
        </div>

        <!-- Sign Out -->
        <div class="text-center">
          <button class="k-btn k-btn-outline" @click="logout" id="logout-btn">
            Sign Out 👋
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '@/services/supabase.js'

export default {
  name: 'ProfilePage',
  setup() {
    const router = useRouter()
    const showToast = inject('showToast')
    const user = inject('user')
    const profile = ref({ display_name: '', email: '', partner_code: '' })
    const partner = ref(null)
    const editName = ref('')
    const saving = ref(false)

    onMounted(async () => {
      if (user.value) {
        const { data } = await supabase.from('profiles').select('*').eq('id', user.value.id).single()
        if (data) {
          profile.value = data
          editName.value = data.display_name || ''

          if (data.partner_id) {
            const { data: p } = await supabase.from('profiles').select('display_name').eq('id', data.partner_id).single()
            if (p) partner.value = p
          }
        }
      }
    })

    async function updateProfile() {
      saving.value = true
      try {
        await supabase.from('profiles').update({ display_name: editName.value }).eq('id', user.value.id)
        profile.value.display_name = editName.value
        showToast('Profile updated! ✨')
      } catch (e) {
        showToast('Failed to update profile')
      } finally {
        saving.value = false
      }
    }

    async function logout() {
      await supabase.auth.signOut()
      router.push('/')
    }

    return { profile, partner, editName, saving, updateProfile, logout }
  }
}
</script>
