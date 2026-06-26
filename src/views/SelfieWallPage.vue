<template>
  <div class="container py-4">
    <div class="k-page-header">
      <h1>📸 Selfie Wall</h1>
      <p>Your shared photo memories</p>
    </div>

    <!-- Upload Button + Random Memory -->
    <div class="d-flex justify-content-center gap-2 mb-4 flex-wrap">
      <button class="k-btn k-btn-primary" @click="showUpload = true" id="upload-selfie-btn">
        📸 Upload Selfie
      </button>
      <button class="k-btn k-btn-soft" @click="showRandomMemory" id="random-memory-btn">
        🎲 Random Memory
      </button>
    </div>

    <!-- Upload Modal -->
    <div v-if="showUpload" class="k-modal-backdrop" @click.self="showUpload = false">
      <div class="k-modal">
        <div class="k-modal-header">
          <h3>📸 Upload Selfie</h3>
          <button class="k-modal-close" @click="showUpload = false">&times;</button>
        </div>
        <div class="k-form-group">
          <label class="k-label">Select Image</label>
          <input type="file" class="k-input" accept="image/*" @change="handleFileSelect" id="selfie-file-input" />
        </div>
        <div v-if="previewUrl" class="mb-3 text-center">
          <img :src="previewUrl" style="max-width:100%; max-height:250px; border-radius:var(--k-radius-sm); object-fit:cover;" alt="Preview" />
        </div>
        <div class="k-form-group">
          <label class="k-label" for="selfie-caption">Caption (optional)</label>
          <input class="k-input" id="selfie-caption" v-model="caption" placeholder="Add a cute caption 💕" />
        </div>
        <button class="k-btn k-btn-primary w-100 justify-content-center" @click="uploadSelfie" :disabled="!selectedFile || uploading" id="confirm-upload-btn">
          {{ uploading ? 'Uploading...' : 'Upload ✨' }}
        </button>
      </div>
    </div>

    <!-- Random Memory Modal -->
    <div v-if="showRandom" class="k-modal-backdrop" @click.self="showRandom = false">
      <div class="k-modal" style="text-align:center;">
        <div class="k-modal-header">
          <h3>🎲 Random Memory</h3>
          <button class="k-modal-close" @click="showRandom = false">&times;</button>
        </div>
        <div v-if="randomSelfie">
          <img :src="randomSelfie.image_url" style="width:100%; max-height:350px; object-fit:cover; border-radius:var(--k-radius-sm);" :alt="randomSelfie.caption || 'Memory'" />
          <p style="margin-top:1rem; font-weight:600;">{{ randomSelfie.caption || '💕' }}</p>
          <p style="font-size:0.8rem; color:var(--k-text-muted);">{{ formatDate(randomSelfie.created_at) }}</p>
        </div>
        <div v-else class="k-empty">
          <p>No memories yet!</p>
        </div>
        <button class="k-btn k-btn-soft mt-2" @click="showRandomMemory">🔀 Another one</button>
      </div>
    </div>

    <!-- Selfie Grid -->
    <div v-if="selfies.length" class="k-image-grid">
      <div v-for="selfie in selfies" :key="selfie.id" class="k-card p-0" style="overflow:hidden;">
        <div class="k-image-card">
          <img :src="selfie.image_url" :alt="selfie.caption || 'Selfie'" />
          <div class="k-image-overlay">
            <p style="margin:0; font-size:0.85rem; font-weight:600;">{{ selfie.caption || '' }}</p>
          </div>
        </div>
        <div class="p-2">
          <div class="d-flex justify-content-between align-items-center">
            <span style="font-size:0.75rem; color:var(--k-text-muted);">{{ formatDate(selfie.created_at) }}</span>
            <div class="k-reactions">
              <button v-for="emoji in ['❤️', '😍', '🔥', '😂']" :key="emoji" class="k-reaction" :class="{ active: selfie.userReaction === emoji }" @click="reactToSelfie(selfie, emoji)">
                {{ emoji }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="k-empty">
      <div class="k-empty-icon">📷</div>
      <p>No selfies yet! Upload your first one above.</p>
    </div>
  </div>
</template>

<script>
import { ref, inject, onMounted } from 'vue'
import { supabase } from '@/services/supabase.js'

export default {
  name: 'SelfieWallPage',
  setup() {
    const showToast = inject('showToast')
    const user = inject('user')
    const selfies = ref([])
    const showUpload = ref(false)
    const showRandom = ref(false)
    const selectedFile = ref(null)
    const previewUrl = ref('')
    const caption = ref('')
    const uploading = ref(false)
    const randomSelfie = ref(null)

    onMounted(loadSelfies)

    async function loadSelfies() {
      try {
        const { data } = await supabase
          .from('selfies')
          .select('*')
          .order('created_at', { ascending: false })
        if (data) selfies.value = data
      } catch (e) { /* ok */ }
    }

    function handleFileSelect(e) {
      const file = e.target.files[0]
      if (file) {
        selectedFile.value = file
        previewUrl.value = URL.createObjectURL(file)
      }
    }

    async function uploadSelfie() {
      if (!selectedFile.value) return
      uploading.value = true
      try {
        const fileName = `selfies/${user.value.id}/${Date.now()}_${selectedFile.value.name}`
        const { error: uploadError } = await supabase.storage
          .from('kaori-media')
          .upload(fileName, selectedFile.value)
        
        if (uploadError) throw uploadError

        const { data: urlData } = supabase.storage.from('kaori-media').getPublicUrl(fileName)

        await supabase.from('selfies').insert({
          user_id: user.value.id,
          image_url: urlData.publicUrl,
          caption: caption.value || null,
          created_at: new Date().toISOString()
        })

        // Log activity
        await supabase.from('activity_feed').insert({
          user_id: user.value.id,
          action: 'uploaded_selfie',
          icon: '📸',
          text: 'Uploaded a selfie',
          created_at: new Date().toISOString()
        })

        showToast('Selfie uploaded! 📸')
        showUpload.value = false
        selectedFile.value = null
        previewUrl.value = ''
        caption.value = ''
        await loadSelfies()
      } catch (e) {
        showToast('Upload failed: ' + (e.message || 'Unknown error'))
      } finally {
        uploading.value = false
      }
    }

    async function reactToSelfie(selfie, emoji) {
      try {
        await supabase.from('selfie_reactions').upsert({
          selfie_id: selfie.id,
          user_id: user.value?.id,
          reaction: emoji,
          created_at: new Date().toISOString()
        })
        selfie.userReaction = emoji
        showToast(`Reacted ${emoji}`)
      } catch (e) { /* ok */ }
    }

    async function showRandomMemory() {
      showRandom.value = true
      try {
        const { data } = await supabase.from('selfies').select('*')
        if (data?.length) {
          randomSelfie.value = data[Math.floor(Math.random() * data.length)]
        }
      } catch (e) { /* ok */ }
    }

    function formatDate(d) {
      if (!d) return ''
      return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    }

    return {
      selfies, showUpload, showRandom, selectedFile, previewUrl,
      caption, uploading, randomSelfie,
      handleFileSelect, uploadSelfie, reactToSelfie, showRandomMemory, formatDate
    }
  }
}
</script>
