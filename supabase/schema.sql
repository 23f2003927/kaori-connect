-- ═══════════════════════════════════════════
-- Kaori Database Schema
-- Run this in Supabase SQL Editor
-- ═══════════════════════════════════════════

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ─── Profiles ─────────────────────────────
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  display_name TEXT NOT NULL DEFAULT '',
  email TEXT,
  partner_code TEXT UNIQUE NOT NULL,
  partner_id UUID REFERENCES profiles(id),
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Couples ──────────────────────────────
CREATE TABLE IF NOT EXISTS couples (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user1_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  user2_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user1_id, user2_id)
);

-- ─── Questions ────────────────────────────
CREATE TABLE IF NOT EXISTS questions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  text TEXT NOT NULL,
  category TEXT NOT NULL DEFAULT 'Random',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Question Answers ─────────────────────
CREATE TABLE IF NOT EXISTS question_answers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  question_id UUID REFERENCES questions(id),
  question_text TEXT NOT NULL,
  category TEXT DEFAULT 'Random',
  answer TEXT NOT NULL,
  partner_answer TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Selfies ──────────────────────────────
CREATE TABLE IF NOT EXISTS selfies (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  caption TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Selfie Reactions ─────────────────────
CREATE TABLE IF NOT EXISTS selfie_reactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  selfie_id UUID NOT NULL REFERENCES selfies(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  reaction TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(selfie_id, user_id)
);

-- ─── Wardrobe Items ───────────────────────
CREATE TABLE IF NOT EXISTS wardrobe_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  category TEXT DEFAULT 'Tops',
  color TEXT,
  season TEXT DEFAULT 'All Seasons',
  occasion TEXT DEFAULT 'Casual',
  favorite BOOLEAN DEFAULT FALSE,
  image_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Outfits ──────────────────────────────
CREATE TABLE IF NOT EXISTS outfits (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  favorite BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Outfit Items ─────────────────────────
CREATE TABLE IF NOT EXISTS outfit_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  outfit_id UUID NOT NULL REFERENCES outfits(id) ON DELETE CASCADE,
  wardrobe_item_id UUID NOT NULL REFERENCES wardrobe_items(id) ON DELETE CASCADE
);

-- ─── Wardrobe Requests ────────────────────
CREATE TABLE IF NOT EXISTS wardrobe_requests (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  from_user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  to_user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  item_id UUID REFERENCES wardrobe_items(id) ON DELETE SET NULL,
  message TEXT,
  status TEXT DEFAULT 'Pending' CHECK (status IN ('Pending', 'Accepted', 'Declined', 'Worn')),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Health Plans ─────────────────────────
CREATE TABLE IF NOT EXISTS health_plans (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  type TEXT NOT NULL,
  target TEXT,
  status TEXT DEFAULT 'Not Started' CHECK (status IN ('Not Started', 'In Progress', 'Completed')),
  streak INTEGER DEFAULT 0,
  last_completed TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Health Logs ──────────────────────────
CREATE TABLE IF NOT EXISTS health_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  plan_id UUID NOT NULL REFERENCES health_plans(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  status TEXT NOT NULL,
  notes TEXT,
  logged_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Widgets ──────────────────────────────
CREATE TABLE IF NOT EXISTS widgets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  widget_type TEXT NOT NULL,
  position INTEGER DEFAULT 0,
  config JSONB DEFAULT '{}',
  enabled BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Notifications ────────────────────────
CREATE TABLE IF NOT EXISTS notifications (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  type TEXT DEFAULT 'general',
  message TEXT NOT NULL,
  read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Activity Feed ────────────────────────
CREATE TABLE IF NOT EXISTS activity_feed (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  action TEXT NOT NULL,
  icon TEXT DEFAULT '💕',
  text TEXT NOT NULL,
  user_name TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Game Scores ──────────────────────────
CREATE TABLE IF NOT EXISTS game_scores (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  game_type TEXT NOT NULL,
  score INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Relationship Stats ──────────────────
CREATE TABLE IF NOT EXISTS relationship_stats (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  couple_id UUID REFERENCES couples(id) ON DELETE CASCADE,
  days_together INTEGER DEFAULT 0,
  questions_answered INTEGER DEFAULT 0,
  selfies_shared INTEGER DEFAULT 0,
  goals_completed INTEGER DEFAULT 0,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Indexes ──────────────────────────────
CREATE INDEX IF NOT EXISTS idx_profiles_partner_code ON profiles(partner_code);
CREATE INDEX IF NOT EXISTS idx_question_answers_user ON question_answers(user_id);
CREATE INDEX IF NOT EXISTS idx_selfies_user ON selfies(user_id);
CREATE INDEX IF NOT EXISTS idx_wardrobe_items_user ON wardrobe_items(user_id);
CREATE INDEX IF NOT EXISTS idx_health_plans_user ON health_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_feed_created ON activity_feed(created_at DESC);

-- ─── Row Level Security ───────────────────
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE couples ENABLE ROW LEVEL SECURITY;
ALTER TABLE question_answers ENABLE ROW LEVEL SECURITY;
ALTER TABLE selfies ENABLE ROW LEVEL SECURITY;
ALTER TABLE selfie_reactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE wardrobe_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE outfits ENABLE ROW LEVEL SECURITY;
ALTER TABLE outfit_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE wardrobe_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE health_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE health_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE widgets ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_feed ENABLE ROW LEVEL SECURITY;
ALTER TABLE game_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE relationship_stats ENABLE ROW LEVEL SECURITY;

-- ─── RLS Policies ─────────────────────────
-- Profiles: users can read all, update their own
CREATE POLICY "profiles_read" ON profiles FOR SELECT USING (true);
CREATE POLICY "profiles_insert" ON profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "profiles_update" ON profiles FOR UPDATE USING (auth.uid() = id OR auth.uid() IN (SELECT partner_id FROM profiles WHERE id = profiles.id));

-- Selfies: users in same couple can see each other's
CREATE POLICY "selfies_all" ON selfies FOR ALL USING (true);
CREATE POLICY "question_answers_all" ON question_answers FOR ALL USING (true);
CREATE POLICY "wardrobe_items_all" ON wardrobe_items FOR ALL USING (true);
CREATE POLICY "wardrobe_requests_all" ON wardrobe_requests FOR ALL USING (true);
CREATE POLICY "health_plans_all" ON health_plans FOR ALL USING (true);
CREATE POLICY "health_logs_all" ON health_logs FOR ALL USING (true);
CREATE POLICY "notifications_all" ON notifications FOR ALL USING (true);
CREATE POLICY "activity_feed_all" ON activity_feed FOR ALL USING (true);
CREATE POLICY "couples_all" ON couples FOR ALL USING (true);
CREATE POLICY "widgets_all" ON widgets FOR ALL USING (true);
CREATE POLICY "outfits_all" ON outfits FOR ALL USING (true);
CREATE POLICY "outfit_items_all" ON outfit_items FOR ALL USING (true);
CREATE POLICY "selfie_reactions_all" ON selfie_reactions FOR ALL USING (true);
CREATE POLICY "game_scores_all" ON game_scores FOR ALL USING (true);
CREATE POLICY "relationship_stats_all" ON relationship_stats FOR ALL USING (true);

-- ─── Storage Bucket ───────────────────────
-- Run this separately or in Supabase dashboard:
-- INSERT INTO storage.buckets (id, name, public) VALUES ('kaori-media', 'kaori-media', true);
