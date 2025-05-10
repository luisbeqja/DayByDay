<template>
  <div class="preferences">
    <h1>Your Preferences</h1>
    <PreferencesForm @submit="handlePreferencesSubmit" />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import PreferencesForm from '../components/PreferencesForm.vue'
import type { UserPreferences } from '../types'

const router = useRouter()

const handlePreferencesSubmit = async (preferences: UserPreferences) => {
  try {
    const response = await fetch('http://localhost:5000/api/preferences', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(preferences)
    })

    if (!response.ok) {
      throw new Error('Failed to save preferences')
    }

    const data = await response.json()
    if (data.success) {
      router.push('/agent')
    }
  } catch (error) {
    console.error('Error saving preferences:', error)
    // TODO: Add error notification
  }
}
</script>

<style scoped>
.preferences {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}
</style> 