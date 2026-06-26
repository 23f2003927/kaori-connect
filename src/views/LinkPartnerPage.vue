<template>
  <div class="k-auth-page">
    <div class="k-card k-auth-card" style="max-width:500px;">
      <div class="k-auth-logo">
        <h1>🔗 Link Partner</h1>
        <p>Connect with your special someone</p>
      </div>

      <!-- Show user's own partner code -->
      <div class="k-card mb-4" style="background:var(--k-cream); text-align:center;">
        <p style="font-size:0.85rem; color:var(--k-text-light); margin-bottom:0.5rem;">Your Partner Code</p>
        <div style="font-size:1.8rem; font-weight:800; font-family:var(--k-font-display); letter-spacing:3px; color:var(--k-pink-dark);">
          {{ partnerCode || '...' }}
        </div>
        <p style="font-size:0.8rem; color:var(--k-text-muted); margin-top:0.5rem;">Share this with your partner 💕</p>
      </div>

      <div class="k-divider">or enter their code</div>

      <!-- Enter partner's code -->
      <form @submit.prevent="linkPartner" id="link-partner-form">
        <div class="k-form-group">
          <label class="k-label" for="partner-code-input">Partner's Code</label>
          <input class="k-input" id="partner-code-input" type="text" v-model="inputCode" placeholder="K-XXXXXX" required style="text-align:center; font-size:1.2rem; letter-spacing:2px; text-transform:uppercase;" />
        </div>

        <div v-if="error" class="k-badge k-badge-pink mb-3 d-block text-center" style="padding:0.5rem;">
          {{ error }}
        </div>
        <div v-if="success" class="k-badge k-badge-mint mb-3 d-block text-center" style="padding:0.5rem;">
          {{ success }}
        </div>

        <button type="submit" class="k-btn k-btn-primary w-100 justify-content-center" id="link-submit" :disabled="loading">
          {{ loading ? 'Linking...' : 'Link Partner 💕' }}
        </button>
      </form>

      <div class="text-center mt-3">
        <button class="k-btn k-btn-soft" @click="logout" id="link-logout">Sign Out</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '@/services/supabase.js'

export default {
  name: 'LinkPartnerPage',
  setup() {
    const router = useRouter()
    const showToast = inject('showToast')
    const partnerCode = ref('')
    const inputCode = ref('')
    const error = ref('')
    const success = ref('')
    const loading = ref(false)

    onMounted(async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (user) {
        const { data } = await supabase.from('profiles').select('partner_code').eq('id', user.id).single()
        if (data) partnerCode.value = data.partner_code
      }
    })

    async function linkPartner() {
      error.value = ''
      success.value = ''
      loading.value = true
      try {
        const { data: { user } } = await supabase.auth.getUser()
        const code = inputCode.value.trim().toUpperCase()

        // Find partner by code
        const { data: partner } = await supabase
          .from('profiles')
          .select('id, display_name')
          .eq('partner_code', code)
          .single()

        if (!partner) throw new Error('Partner code not found')
        if (partner.id === user.id) throw new Error("You can't link with yourself!")

        // Create couple record
        await supabase.from('couples').insert({
          user1_id: user.id,
          user2_id: partner.id,
          created_at: new Date().toISOString()
        })

        // Update both profiles with partner_id
        await supabase.from('profiles').update({ partner_id: partner.id }).eq('id', user.id)
        await supabase.from('profiles').update({ partner_id: user.id }).eq('id', partner.id)

        success.value = `Linked with ${partner.display_name}! 💕`
        showToast(`You're now connected with ${partner.display_name}! 💕`)
        setTimeout(() => router.push('/dashboard'), 1500)
      } catch (e) {
        error.value = e.message || 'Failed to link partner'
      } finally {
        loading.value = false
      }
    }

    async function logout() {
      await supabase.auth.signOut()
      router.push('/')
    }

    return { partnerCode, inputCode, error, success, loading, linkPartner, logout }
  }
}
</script>
