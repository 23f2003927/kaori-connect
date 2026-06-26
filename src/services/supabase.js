// Supabase configuration for Kaori
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://qfiyvwfqtskdlzoqjybg.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFmaXl2d2ZxdHNrZGx6b3FqeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI0OTA4MjUsImV4cCI6MjA5ODA2NjgyNX0.ZCORpp8wc_lFvGrz4eHY6StwC201xnsHxXDXTJj2ICU'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
