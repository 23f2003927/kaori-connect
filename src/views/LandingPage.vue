<template>
  <div>
    <!-- Hero Section -->
    <section class="k-hero">
      <div class="k-hero-hearts">
        <span v-for="i in 15" :key="i" class="k-hero-heart" :style="heartStyle(i)">💕</span>
      </div>
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6 k-hero-content">
            <div class="k-badge-pink k-badge mb-3 k-pop-in">✨ Your cozy couple space</div>
            <h1 class="k-pop-in">
              Stay connected with your
              <span style="background: var(--k-grad-sunset); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                special someone
              </span>
              💕
            </h1>
            <p class="k-pop-in mb-4">
              Kaori is your shared digital scrapbook — answer fun questions together,
              share selfies, track health goals, coordinate outfits, and make every
              day a little sweeter.
            </p>
            <div class="d-flex gap-3 flex-wrap k-pop-in">
              <router-link to="/register" class="k-btn k-btn-primary" id="hero-get-started">
                Get Started 💕
              </router-link>
              <router-link to="/login" class="k-btn k-btn-outline" id="hero-login">
                Sign In
              </router-link>
            </div>
          </div>
          <div class="col-lg-6 text-center mt-5 mt-lg-0">
            <div class="k-hero-illustration k-float">
              <div class="k-glass p-4" style="max-width:380px; margin:auto;">
                <div class="text-center mb-3" style="font-size:4rem;">💑</div>
                <h3 style="font-size:1.2rem; text-align:center;">Today's Question</h3>
                <p style="color:var(--k-text-light); text-align:center; font-size:0.9rem; margin-bottom:1rem;">
                  "What's one thing about me that always makes you smile?"
                </p>
                <div class="d-flex gap-2 justify-content-center">
                  <span class="k-badge k-badge-pink">🥰 Romantic</span>
                  <span class="k-badge k-badge-lavender">💭 Deep</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="k-features" style="background: var(--k-cream);">
      <div class="container">
        <div class="text-center mb-5">
          <h2 style="font-size:2rem;">Everything you need to stay close 💝</h2>
          <p style="color:var(--k-text-light); max-width:500px; margin:auto;">
            Fun activities and shared moments that bring you closer, every single day.
          </p>
        </div>
        <div class="row g-4">
          <div class="col-md-4 col-6" v-for="feature in features" :key="feature.title">
            <div class="k-card k-feature-card">
              <div class="k-feature-icon">{{ feature.icon }}</div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section style="padding:5rem 0; text-align:center; background: var(--k-grad-hero);">
      <div class="container">
        <h2 style="font-size:2rem; margin-bottom:1rem;">Ready to start your Kaori journey? 💕</h2>
        <p style="color:var(--k-text-light); max-width:450px; margin:0 auto 2rem;">
          Create your space, invite your partner, and make every day special.
        </p>
        <router-link to="/register" class="k-btn k-btn-primary" id="cta-register" style="font-size:1.1rem; padding:0.8rem 2rem;">
          Create Your Space ✨
        </router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer style="padding:2rem 0; text-align:center; background: var(--k-bg-card); border-top:1px solid var(--k-border);">
      <p style="color:var(--k-text-muted); margin:0; font-size:0.85rem;">
        💕 Kaori — Made with love for couples everywhere
      </p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
  setup() {
    const features = [
      { icon: '💭', title: 'Daily Questions', desc: 'Fun prompts to discover new things about each other' },
      { icon: '📸', title: 'Selfie Wall', desc: 'Share moments and react to each other\'s selfies' },
      { icon: '👗', title: 'Shared Wardrobe', desc: 'Coordinate outfits and send style requests' },
      { icon: '💪', title: 'Health Goals', desc: 'Track fitness goals and cheer each other on' },
      { icon: '🎮', title: 'Couple Games', desc: 'Play fun games and compete lovingly' },
      { icon: '📊', title: 'Widgets', desc: 'Customize your dashboard with love meters and trackers' }
    ]

    function heartStyle(i) {
      return {
        left: `${Math.random() * 100}%`,
        animationDelay: `${i * 1.2}s`,
        animationDuration: `${12 + Math.random() * 8}s`,
        fontSize: `${1 + Math.random() * 1.5}rem`
      }
    }

    return { features, heartStyle }
  }
}
</script>
