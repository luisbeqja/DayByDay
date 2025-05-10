<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import type { UserPreferences, Activity } from './types';

const router = useRouter();

const handlePreferencesSubmit = async (preferences: UserPreferences) => {
  try {
    const response = await fetch('http://localhost:5000/api/preferences', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(preferences)
    });

    if (!response.ok) {
      throw new Error('Failed to save preferences');
    }

    const data = await response.json();
    if (data.success) {
      router.push('/agent');
    }
  } catch (error) {
    console.error('Error saving preferences:', error);
    // TODO: Add error notification
  }
};

const formatDuration = (minutes: number) => {
  if (minutes < 60) return `${minutes}min`;
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}min` : `${hours}h`;
};

const formatPrice = (price: number) => {
  if (price === 0) return 'Free';
  return `€${price}`;
};
</script>

<template>
  <div class="app">
    <router-view></router-view>
  </div>
</template>

<style>
.app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.itinerary {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.itinerary h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.activities {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.activity-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  transition: transform 0.2s;
}

.activity-card:hover {
  transform: translateY(-4px);
}

.activity-image {
  width: 200px;
  height: 200px;
  flex-shrink: 0;
}

.activity-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.activity-content {
  padding: 1.5rem;
  flex-grow: 1;
}

.activity-content h3 {
  margin: 0 0 1rem;
  color: #333;
}

.description {
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.activity-details {
  display: flex;
  gap: 1rem;
  color: #666;
  font-size: 0.9rem;
}

.reset-button {
  display: block;
  margin: 3rem auto 0;
  padding: 1rem 2rem;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.reset-button:hover {
  background-color: #444;
}

@media (max-width: 768px) {
  .activity-card {
    flex-direction: column;
  }
  
  .activity-image {
    width: 100%;
    height: 200px;
  }
}
</style>
