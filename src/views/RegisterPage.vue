<template>
  <div class="k-auth-page">
    <div class="k-card k-auth-card">
      <div class="k-auth-logo">
        <h1>💕 Kaori</h1>
        <p>Create your cozy couple space</p>
      </div>

      <form @submit.prevent="handleRegister" id="register-form">
        <div class="k-form-group">
          <label class="k-label" for="reg-name">Display Name</label>
          <input class="k-input" id="reg-name" type="text" v-model="displayName" placeholder="Your cute nickname" required />
        </div>
        <div class="k-form-group">
          <label class="k-label" for="reg-email">Email</label>
          <input class="k-input" id="reg-email" type="email" v-model="email" placeholder="your@email.com" required />
        </div>
        <div class="k-form-group">
          <label class="k-label" for="reg-password">Password</label>
          <input class="k-input" id="reg-password" type="password" v-model="password" placeholder="At least 6 characters" required minlength="6" />
        </div>

        <div v-if="error" class="k-badge k-badge-pink mb-3 d-block text-center" style="padding:0.5rem;">
          {{ error }}
        </div>

        <div v-if="success" class="k-badge k-badge-mint mb-3 d-block text-center" style="padding:0.5rem;">
          {{ success }}
        </div>

        <button type="submit" class="k-btn k-btn-primary w-100 justify-content-center" id="register-submit" :disabled="loading">
          {{ loading ? 'Creating...' : 'Create Account ✨' }}
        </button>
      </form>

      <div class="k-divider">or</div>

      <div class="text-center">
        <p style="color:var(--k-text-light); font-size:0.9rem;">
          Already have an account?
          <router-link to="/login" style="color:var(--k-pink-dark); font-weight:600;">Sign in 💕</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '@/services/supabase.js'

export default {
  name: 'RegisterPage',
  setup() {
    const router = useRouter()
    const displayName = ref('')
    const email = ref('')
    const password = ref('')
    const error = ref('')
    const success = ref('')
    const loading = ref(false)

    async function handleRegister() {
      error.value = ''
      success.value = ''
      loading.value = true
      try {
        const { data, error: authError } = await supabase.auth.signUp({
          email: email.value,
          password: password.value,
          options: {
            data: { display_name: displayName.value }
          }
        })
        if (authError) throw authError

        // Create profile with partner code
        if (data.user) {
          const partnerCode = generatePartnerCode()
          await supabase.from('profiles').upsert({
            id: data.user.id,
            display_name: displayName.value,
            email: email.value,
            partner_code: partnerCode,
            created_at: new Date().toISOString()
          })
        }

        // If user has a session (no email confirmation required), go to link-partner
        if (data.session) {
          success.value = 'Account created! Redirecting to partner linking...'
          setTimeout(() => router.push('/link-partner'), 1000)
        } else {
          // Email confirmation required
          success.value = 'Account created! Check your email to confirm, then sign in.'
          setTimeout(() => router.push('/login'), 2500)
        }
      } catch (e) {
        error.value = e.message || 'Failed to create account'
      } finally {
        loading.value = false
      }
    }

    function generatePartnerCode() {
      const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
      let code = 'K-'
      for (let i = 0; i < 6; i++) {
        code += chars[Math.floor(Math.random() * chars.length)]
      }
      return code
    }

    return { displayName, email, password, error, success, loading, handleRegister }
  }
}
</script>
