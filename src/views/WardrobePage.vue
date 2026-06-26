<template>
  <div class="container py-4">
    <div class="k-page-header">
      <h1>👗 Shared Wardrobe</h1>
      <p>Browse, share, and coordinate outfits</p>
    </div>

    <!-- Tabs -->
    <div class="k-pills justify-content-center mb-4">
      <button class="k-pill" :class="{ active: tab === 'items' }" @click="tab = 'items'">👕 My Items</button>
      <button class="k-pill" :class="{ active: tab === 'partner' }" @click="tab = 'partner'">💕 Partner's</button>
      <button class="k-pill" :class="{ active: tab === 'outfits' }" @click="tab = 'outfits'">👔 Outfits</button>
      <button class="k-pill" :class="{ active: tab === 'requests' }" @click="tab = 'requests'">📩 Requests</button>
    </div>

    <!-- Add Item Button -->
    <div class="text-center mb-4" v-if="tab === 'items'">
      <button class="k-btn k-btn-primary" @click="showAddItem = true" id="add-item-btn">
        ➕ Add Clothing Item
      </button>
    </div>

    <!-- Add Item Modal -->
    <div v-if="showAddItem" class="k-modal-backdrop" @click.self="showAddItem = false">
      <div class="k-modal">
        <div class="k-modal-header">
          <h3>👕 Add Clothing Item</h3>
          <button class="k-modal-close" @click="showAddItem = false">&times;</button>
        </div>
        <div class="k-form-group">
          <label class="k-label">Image</label>
          <input type="file" class="k-input" accept="image/*" @change="handleItemImage" id="item-image-input" />
          <div v-if="itemPreview" class="mt-2 text-center">
            <img :src="itemPreview" style="max-height:150px; border-radius:var(--k-radius-sm);" alt="Preview" />
          </div>
        </div>
        <div class="k-form-group">
          <label class="k-label" for="item-name">Name</label>
          <input class="k-input" id="item-name" v-model="newItem.name" placeholder="Blue Hoodie" />
        </div>
        <div class="row g-2">
          <div class="col-6 k-form-group">
            <label class="k-label">Category</label>
            <select class="k-input" v-model="newItem.category">
              <option v-for="c in itemCategories" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>
          <div class="col-6 k-form-group">
            <label class="k-label">Color</label>
            <input class="k-input" v-model="newItem.color" placeholder="Blue" />
          </div>
        </div>
        <div class="row g-2">
          <div class="col-6 k-form-group">
            <label class="k-label">Season</label>
            <select class="k-input" v-model="newItem.season">
              <option v-for="s in seasons" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div class="col-6 k-form-group">
            <label class="k-label">Occasion</label>
            <select class="k-input" v-model="newItem.occasion">
              <option v-for="o in occasions" :key="o" :value="o">{{ o }}</option>
            </select>
          </div>
        </div>
        <div class="k-form-group">
          <label class="d-flex align-items-center gap-2" style="cursor:pointer;">
            <input type="checkbox" v-model="newItem.favorite" />
            <span>❤️ Mark as favorite</span>
          </label>
        </div>
        <button class="k-btn k-btn-primary w-100 justify-content-center" @click="addItem" :disabled="!newItem.name || addingItem" id="save-item-btn">
          {{ addingItem ? 'Saving...' : 'Save Item ✨' }}
        </button>
      </div>
    </div>

    <!-- Items Grid -->
    <div v-if="tab === 'items' || tab === 'partner'" class="k-grid k-grid-3">
      <div v-for="item in displayItems" :key="item.id" class="k-card p-0" style="overflow:hidden;">
        <div style="aspect-ratio:3/4; overflow:hidden;">
          <img :src="item.image_url || '/placeholder-clothing.svg'" :alt="item.name" style="width:100%; height:100%; object-fit:cover;" />
        </div>
        <div class="p-3">
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <h4 style="font-size:0.95rem; margin:0;">{{ item.name }}</h4>
              <span style="font-size:0.8rem; color:var(--k-text-muted);">{{ item.category }}</span>
            </div>
            <span v-if="item.favorite" style="font-size:1.2rem;">❤️</span>
          </div>
          <div class="d-flex flex-wrap gap-1 mt-2">
            <span class="k-badge k-badge-pink" v-if="item.color">{{ item.color }}</span>
            <span class="k-badge k-badge-lavender" v-if="item.season">{{ item.season }}</span>
          </div>
          <button v-if="tab === 'partner'" class="k-btn k-btn-soft mt-2 w-100 justify-content-center" @click="sendRequest(item)" style="font-size:0.8rem;">
            📩 Request to wear
          </button>
        </div>
      </div>
    </div>

    <!-- Outfits Tab -->
    <div v-if="tab === 'outfits'">
      <div class="text-center mb-3">
        <button class="k-btn k-btn-primary" @click="showCreateOutfit = true" id="create-outfit-btn">
          ✨ Create Outfit
        </button>
      </div>
      <div class="k-grid k-grid-2">
        <div v-for="outfit in outfits" :key="outfit.id" class="k-card">
          <h4 style="font-size:1rem;">{{ outfit.name }}</h4>
          <div class="d-flex gap-2 flex-wrap mt-2">
            <div v-for="oi in outfit.items" :key="oi.id" class="text-center" style="width:70px;">
              <div style="width:60px; height:60px; border-radius:var(--k-radius-sm); overflow:hidden; margin:0 auto;">
                <img :src="oi.image_url || '/placeholder-clothing.svg'" style="width:100%; height:100%; object-fit:cover;" :alt="oi.name" />
              </div>
              <span style="font-size:0.7rem;">{{ oi.name }}</span>
            </div>
          </div>
        </div>
      </div>
      <div v-if="!outfits.length" class="k-empty">
        <div class="k-empty-icon">👔</div>
        <p>No outfits yet. Create your first one!</p>
      </div>
    </div>

    <!-- Requests Tab -->
    <div v-if="tab === 'requests'">
      <div v-for="req in requests" :key="req.id" class="k-card mb-3">
        <div class="d-flex align-items-center gap-3">
          <span style="font-size:2rem;">👕</span>
          <div style="flex:1;">
            <p style="font-weight:600; margin:0;">{{ req.message }}</p>
            <span style="font-size:0.8rem; color:var(--k-text-muted);">{{ formatDate(req.created_at) }}</span>
          </div>
          <span class="k-badge" :class="requestBadge(req.status)">{{ req.status }}</span>
        </div>
        <div v-if="req.status === 'Pending' && req.to_user_id === userId" class="d-flex gap-2 mt-2 justify-content-end">
          <button class="k-btn k-btn-soft" @click="updateRequest(req, 'Accepted')" style="font-size:0.8rem;">✅ Accept</button>
          <button class="k-btn k-btn-outline" @click="updateRequest(req, 'Declined')" style="font-size:0.8rem;">❌ Decline</button>
        </div>
      </div>
      <div v-if="!requests.length" class="k-empty">
        <div class="k-empty-icon">📩</div>
        <p>No wardrobe requests</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, inject, onMounted } from 'vue'
import { supabase } from '@/services/supabase.js'

export default {
  name: 'WardrobePage',
  setup() {
    const showToast = inject('showToast')
    const user = inject('user')
    const tab = ref('items')
    const myItems = ref([])
    const partnerItems = ref([])
    const outfits = ref([])
    const requests = ref([])
    const showAddItem = ref(false)
    const showCreateOutfit = ref(false)
    const itemPreview = ref('')
    const itemFile = ref(null)
    const addingItem = ref(false)
    const userId = computed(() => user.value?.id)

    const itemCategories = ['Tops', 'Bottoms', 'Dresses', 'Outerwear', 'Shoes', 'Accessories']
    const seasons = ['Spring', 'Summer', 'Autumn', 'Winter', 'All Seasons']
    const occasions = ['Casual', 'Formal', 'Sports', 'Party', 'Date Night', 'Work']

    const newItem = ref({ name: '', category: 'Tops', color: '', season: 'All Seasons', occasion: 'Casual', favorite: false })

    const displayItems = computed(() => tab.value === 'partner' ? partnerItems.value : myItems.value)

    onMounted(loadData)

    async function loadData() {
      try {
        const { data } = await supabase.from('wardrobe_items').select('*').eq('user_id', user.value?.id).order('created_at', { ascending: false })
        if (data) myItems.value = data
      } catch (e) { /* ok */ }

      try {
        const { data: profile } = await supabase.from('profiles').select('partner_id').eq('id', user.value?.id).single()
        if (profile?.partner_id) {
          const { data } = await supabase.from('wardrobe_items').select('*').eq('user_id', profile.partner_id)
          if (data) partnerItems.value = data
        }
      } catch (e) { /* ok */ }

      try {
        const { data } = await supabase.from('wardrobe_requests').select('*').order('created_at', { ascending: false })
        if (data) requests.value = data
      } catch (e) { /* ok */ }
    }

    function handleItemImage(e) {
      const file = e.target.files[0]
      if (file) {
        itemFile.value = file
        itemPreview.value = URL.createObjectURL(file)
      }
    }

    async function addItem() {
      addingItem.value = true
      try {
        let imageUrl = null
        if (itemFile.value) {
          const fileName = `wardrobe/${user.value.id}/${Date.now()}_${itemFile.value.name}`
          await supabase.storage.from('kaori-media').upload(fileName, itemFile.value)
          const { data } = supabase.storage.from('kaori-media').getPublicUrl(fileName)
          imageUrl = data.publicUrl
        }

        await supabase.from('wardrobe_items').insert({
          user_id: user.value.id,
          name: newItem.value.name,
          category: newItem.value.category,
          color: newItem.value.color,
          season: newItem.value.season,
          occasion: newItem.value.occasion,
          favorite: newItem.value.favorite,
          image_url: imageUrl,
          created_at: new Date().toISOString()
        })

        showToast('Item added! 👕')
        showAddItem.value = false
        newItem.value = { name: '', category: 'Tops', color: '', season: 'All Seasons', occasion: 'Casual', favorite: false }
        itemPreview.value = ''
        itemFile.value = null
        await loadData()
      } catch (e) {
        showToast('Failed to add item')
      } finally {
        addingItem.value = false
      }
    }

    async function sendRequest(item) {
      try {
        await supabase.from('wardrobe_requests').insert({
          from_user_id: user.value.id,
          to_user_id: item.user_id,
          item_id: item.id,
          message: `Please wear the ${item.name}`,
          status: 'Pending',
          created_at: new Date().toISOString()
        })
        showToast('Request sent! 📩')
      } catch (e) {
        showToast('Failed to send request')
      }
    }

    async function updateRequest(req, status) {
      try {
        await supabase.from('wardrobe_requests').update({ status }).eq('id', req.id)
        req.status = status
        showToast(`Request ${status.toLowerCase()}`)
      } catch (e) { /* ok */ }
    }

    function requestBadge(s) {
      if (s === 'Accepted') return 'k-badge-mint'
      if (s === 'Declined') return 'k-badge-pink'
      if (s === 'Worn') return 'k-badge-lavender'
      return 'k-badge-peach'
    }

    function formatDate(d) {
      if (!d) return ''
      return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }

    return {
      tab, displayItems, outfits, requests, showAddItem, showCreateOutfit,
      itemPreview, newItem, addingItem, userId,
      itemCategories, seasons, occasions,
      handleItemImage, addItem, sendRequest, updateRequest, requestBadge, formatDate
    }
  }
}
</script>
