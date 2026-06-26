<template>
  <div class="container py-4">
    <div class="k-page-header">
      <h1>💭 Daily Questions</h1>
      <p>Discover new things about each other every day</p>
    </div>

    <!-- Category Pills -->
    <div class="k-pills justify-content-center mb-4">
      <button v-for="cat in categories" :key="cat.name" class="k-pill" :class="{ active: selectedCategory === cat.name }" @click="selectCategory(cat.name)" :id="'cat-' + cat.name">
        {{ cat.icon }} {{ cat.name }}
      </button>
    </div>

    <!-- Current Question Card -->
    <div class="row justify-content-center mb-4">
      <div class="col-lg-7">
        <div class="k-card k-pop-in" style="text-align:center;" v-if="currentQuestion">
          <span class="k-badge k-badge-lavender mb-3">{{ selectedCategory }}</span>
          <p style="font-size:1.4rem; font-weight:700; margin-bottom:1.5rem; line-height:1.4;">
            {{ currentQuestion.text }}
          </p>

          <!-- Answer Form -->
          <div v-if="!hasAnswered">
            <textarea class="k-input mb-3" v-model="answer" placeholder="Write your answer here... 💭" rows="3" id="question-answer-input" style="resize:none;"></textarea>
            <button class="k-btn k-btn-primary" @click="submitAnswer" :disabled="!answer.trim() || submitting" id="submit-answer-btn">
              {{ submitting ? 'Sending...' : 'Submit Answer ✨' }}
            </button>
          </div>

          <!-- Both Answered -->
          <div v-else-if="partnerAnswer">
            <div class="row g-3 mt-2">
              <div class="col-6">
                <div class="k-card" style="background:var(--k-pink-light);">
                  <div style="font-size:0.8rem; font-weight:600; color:var(--k-pink-dark); margin-bottom:0.3rem;">Your Answer</div>
                  <p style="margin:0; font-size:0.9rem;">{{ myAnswer }}</p>
                </div>
              </div>
              <div class="col-6">
                <div class="k-card" style="background:var(--k-lavender-light);">
                  <div style="font-size:0.8rem; font-weight:600; color:var(--k-lavender-dark); margin-bottom:0.3rem;">Partner's Answer</div>
                  <p style="margin:0; font-size:0.9rem;">{{ partnerAnswer }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Waiting for partner -->
          <div v-else class="k-card" style="background:var(--k-cream); text-align:center;">
            <p style="margin:0; color:var(--k-text-light);">
              ⏳ Waiting for your partner to answer...
            </p>
            <p style="margin:0.3rem 0 0; font-size:0.8rem; color:var(--k-text-muted);">
              Your answer is hidden until they respond
            </p>
          </div>

          <button class="k-btn k-btn-soft mt-3" @click="getNewQuestion" id="new-question-btn" style="font-size:0.85rem;">
            🔀 New Question
          </button>
        </div>

        <div v-else class="k-spinner"></div>
      </div>
    </div>

    <!-- Question History -->
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <h3 style="font-size:1.1rem; margin-bottom:1rem;">📜 Past Questions</h3>
        <div v-if="history.length">
          <div v-for="item in history" :key="item.id" class="k-card mb-3">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <span class="k-badge k-badge-lavender">{{ item.category }}</span>
              <span style="font-size:0.75rem; color:var(--k-text-muted);">{{ item.date }}</span>
            </div>
            <p style="font-weight:600; margin-bottom:0.8rem;">{{ item.question }}</p>
            <div class="row g-2">
              <div class="col-6">
                <div style="background:var(--k-pink-light); padding:0.6rem; border-radius:var(--k-radius-sm);">
                  <div style="font-size:0.7rem; font-weight:600; color:var(--k-pink-dark);">You</div>
                  <p style="margin:0; font-size:0.85rem;">{{ item.myAnswer }}</p>
                </div>
              </div>
              <div class="col-6">
                <div style="background:var(--k-lavender-light); padding:0.6rem; border-radius:var(--k-radius-sm);">
                  <div style="font-size:0.7rem; font-weight:600; color:var(--k-lavender-dark);">Partner</div>
                  <p style="margin:0; font-size:0.85rem;">{{ item.partnerAnswer }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="k-empty">
          <div class="k-empty-icon">💭</div>
          <p>No question history yet. Answer your first question above!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, inject, onMounted } from 'vue'
import { supabase } from '@/services/supabase.js'

// Default question bank
const questionBank = {
  Funny: [
    "What's the most embarrassing thing you've ever done on a date?",
    "If we were in a zombie apocalypse, what's your survival plan for us?",
    "What animal do you think I'd be and why?",
    "What's the silliest thing that makes you laugh every time?",
    "If we switched bodies for a day, what would you do first?"
  ],
  Deep: [
    "What's one thing about me that always makes you smile?",
    "What does 'home' feel like to you?",
    "What's a dream you've never told anyone about?",
    "What moment made you realize you loved me?",
    "If you could relive one day of our relationship, which would it be?"
  ],
  Romantic: [
    "What's your favorite memory of us together?",
    "What made you fall in love with me?",
    "Describe our perfect evening together.",
    "What song reminds you of us?",
    "What's something small I do that means the world to you?"
  ],
  Future: [
    "Where do you see us in 5 years?",
    "What's one adventure you want us to go on together?",
    "What does your dream home look like?",
    "What tradition do you want us to start?",
    "What skill do you want us to learn together?"
  ],
  Random: [
    "Would you rather have breakfast in Paris or dinner in Tokyo?",
    "What superpower would make our relationship even better?",
    "If we had a theme song, what would it be?",
    "What's one thing on your bucket list we should do together?",
    "If you could describe our love in one word, what would it be?"
  ]
}

export default {
  name: 'QuestionsPage',
  setup() {
    const showToast = inject('showToast')
    const user = inject('user')
    const categories = [
      { name: 'Funny', icon: '😄' },
      { name: 'Deep', icon: '🌊' },
      { name: 'Romantic', icon: '🥰' },
      { name: 'Future', icon: '🔮' },
      { name: 'Random', icon: '🎲' }
    ]
    const selectedCategory = ref('Random')
    const currentQuestion = ref(null)
    const answer = ref('')
    const hasAnswered = ref(false)
    const myAnswer = ref('')
    const partnerAnswer = ref(null)
    const submitting = ref(false)
    const history = ref([])

    onMounted(() => {
      getNewQuestion()
      loadHistory()
    })

    function selectCategory(cat) {
      selectedCategory.value = cat
      getNewQuestion()
    }

    function getNewQuestion() {
      const questions = questionBank[selectedCategory.value] || questionBank.Random
      const text = questions[Math.floor(Math.random() * questions.length)]
      currentQuestion.value = { text, category: selectedCategory.value, id: Date.now() }
      hasAnswered.value = false
      answer.value = ''
      myAnswer.value = ''
      partnerAnswer.value = null
    }

    async function submitAnswer() {
      if (!answer.value.trim()) return
      submitting.value = true
      try {
        await supabase.from('question_answers').insert({
          user_id: user.value?.id,
          question_text: currentQuestion.value.text,
          category: selectedCategory.value,
          answer: answer.value.trim(),
          created_at: new Date().toISOString()
        })

        // Log activity
        await supabase.from('activity_feed').insert({
          user_id: user.value?.id,
          action: 'answered_question',
          icon: '💭',
          text: "Answered today's question",
          created_at: new Date().toISOString()
        })

        myAnswer.value = answer.value.trim()
        hasAnswered.value = true
        answer.value = ''
        showToast('Answer submitted! 💭')
      } catch (e) {
        showToast('Could not save answer')
      } finally {
        submitting.value = false
      }
    }

    async function loadHistory() {
      try {
        const { data } = await supabase
          .from('question_answers')
          .select('*')
          .eq('user_id', user.value?.id)
          .order('created_at', { ascending: false })
          .limit(10)
        
        if (data) {
          history.value = data.map(q => ({
            id: q.id,
            category: q.category || 'Random',
            question: q.question_text,
            myAnswer: q.answer,
            partnerAnswer: q.partner_answer || '—',
            date: new Date(q.created_at).toLocaleDateString()
          }))
        }
      } catch (e) { /* tables may not exist yet */ }
    }

    return {
      categories, selectedCategory, currentQuestion, answer,
      hasAnswered, myAnswer, partnerAnswer, submitting, history,
      selectCategory, getNewQuestion, submitAnswer
    }
  }
}
</script>
