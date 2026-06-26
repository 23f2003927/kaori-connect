<template>
  <div class="k-auth-page">
    <div class="k-card k-auth-card">
      <div class="k-auth-logo">
        <h1>💕 Kaori</h1>
        <p>Welcome back! Sign in to your space.</p>
      </div>

      <form @submit.prevent="handleLogin" id="login-form">
        <div class="k-form-group">
          <label class="k-label" for="login-email">Email</label>
          <input class="k-input" id="login-email" type="email" v-model="email" placeholder="your@email.com" required />
        </div>
        <div class="k-form-group">
          <label class="k-label" for="login-password">Password</label>
          <input class="k-input" id="login-password" type="password" v-model="password" placeholder="••••••••" required />
        </div>

        <div v-if="error" class="k-badge k-badge-pink mb-3 d-block text-center" style="padding:0.5rem;">
          {{ error }}
        </div>

        <button type="submit" class="k-btn k-btn-primary w-100 justify-content-center" id="login-submit" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign In 💕' }}
        </button>
      </form>

      <div class="k-divider">or</div>

      <div class="text-center">
        <p style="color:var(--k-text-light); font-size:0.9rem;">
          Don't have an account?
          <router-link to="/register" style="color:var(--k-pink-dark); font-weight:600;">Create one ✨</router-link>
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
  name: 'LoginPage',
  setup() {
    const router = useRouter()
    const email = ref('')
    const password = ref('')
    const error = ref('')
    const loading = ref(false)

    async function handleLogin() {
      error.value = ''
      loading.value = true
      try {
        const { data: authData, error: authError } = await supabase.auth.signInWithPassword({
          email: email.value,
          password: password.value
        })
        if (authError) throw authError

        // Check if user has a linked partner
        const { data: profile } = await supabase
          .from('profiles')
          .select('partner_id')
          .eq('id', authData.user.id)
          .single()

        if (profile && profile.partner_id) {
          router.push('/dashboard')
        } else {
          router.push('/link-partner')
        }
      } catch (e) {
        error.value = e.message || 'Failed to sign in'
      } finally {
        loading.value = false
      }
    }

    return { email, password, error, loading, handleLogin }
  }
}
</script>
