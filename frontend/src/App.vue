<script setup lang="ts">
import { ref, computed } from 'vue';
import WelcomeScreen from './components/WelcomeScreen.vue';
import PreferencesForm from './components/PreferencesForm.vue';
import { mockActivities } from './data/mockActivities';
import type { UserPreferences, Activity } from './types';

type Step = 'welcome' | 'preferences' | 'itinerary';
const currentStep = ref<Step>('welcome');

const handlePreferencesSubmit = (preferences: UserPreferences) => {
  // In a real app, this would call an API to get personalized suggestions
  // For now, we'll just filter the mock activities based on preferences
  suggestedActivities.value = mockActivities
    .filter(activity => {
      // Filter by interests
      if (!preferences.interests.includes(activity.category)) {
        return false;
      }
      
      // Filter by time of day based on schedule
      const workStartHour = parseInt(preferences.schedule.workStartTime.split(':')[0]);
      const workEndHour = parseInt(preferences.schedule.workEndTime.split(':')[0]);
      const preferredStartHour = parseInt(preferences.preferredStartTime.split(':')[0]);
      const preferredEndHour = parseInt(preferences.preferredEndTime.split(':')[0]);
      
      // If it's a morning activity, check if it fits before work/study
      if (activity.timeOfDay === 'morning') {
        if (preferredStartHour >= workStartHour) return false;
      }
      
      // If it's an afternoon activity, check if it fits during break time
      if (activity.timeOfDay === 'afternoon') {
        const breakHour = parseInt(preferences.schedule.breakTime.split(':')[0]);
        const breakEndHour = breakHour + Math.floor(preferences.schedule.breakDuration / 60);
        if (activity.duration > preferences.schedule.breakDuration) return false;
      }
      
      // If it's an evening activity or any time activity, check if it fits after work/study
      if (activity.timeOfDay === 'evening' || activity.timeOfDay === 'any') {
        if (preferredStartHour < workEndHour) return false;
        if (preferredEndHour < workEndHour) return false;
      }
      
      return true;
    })
    .sort((a, b) => {
      // Prioritize activities based on pace preference
      if (preferences.pace === 'relaxed') {
        return a.duration - b.duration; // Shorter activities first
      } else if (preferences.pace === 'active') {
        return b.duration - a.duration; // Longer activities first
      }
      return 0; // No specific sorting for moderate pace
    })
    .slice(0, 3); // Limit to 3 activities for now
};

const suggestedActivities = ref<Activity[]>([]);

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

const resetApp = () => {
  currentStep.value = 'welcome';
  suggestedActivities.value = [];
};
</script>

<template>
  <div class="app">
    <WelcomeScreen
      v-if="currentStep === 'welcome'"
      @start="currentStep = 'preferences'"
    />
    
    <PreferencesForm
      v-else-if="currentStep === 'preferences'"
      @submit="handlePreferencesSubmit"
    />
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
