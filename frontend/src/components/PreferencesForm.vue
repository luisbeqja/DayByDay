<template>
  <div class="preferences-form">
    <h2>Tell me about your daily routine</h2>
    
    <form @submit.prevent="submitPreferences">
      <div class="form-section occupation-section">
        <h3>What's your occupation?</h3>
        <div class="occupation-options">
          <label 
            v-for="option in occupationOptions" 
            :key="option.value" 
            class="occupation-card"
            :class="{ 'selected': selectedOccupation === option.value }"
          >
            <input
              type="radio"
              v-model="selectedOccupation"
              :value="option.value"
              required
              class="radio-input"
            />
            <div class="occupation-content">
              <span class="occupation-title">{{ option.label }}</span>
              <span class="occupation-emoji">{{ option.emoji }}</span>
            </div>
          </label>
        </div>
      </div>

      <div class="form-section">
        <h3>What's your daily schedule?</h3>
        <div class="schedule-grid">
          <div class="time-field">
            <label>When do you start your day?</label>
            <input type="time" v-model="schedule.workStartTime" required />
          </div>
          <div class="time-field">
            <label>When do you end your day?</label>
            <input type="time" v-model="schedule.workEndTime" required />
          </div>
          <div class="time-field">
            <label>When do you usually take your break?</label>
            <input type="time" v-model="schedule.breakTime" required />
          </div>
          <div class="time-field">
            <label>How long is your break? (minutes)</label>
            <input 
              type="number" 
              v-model="schedule.breakDuration" 
              min="15" 
              max="120" 
              step="15" 
              required 
            />
          </div>
        </div>
      </div>

      <div class="form-section">
        <h3>What interests you in your free time?</h3>
        <div class="interests-grid">
          <label v-for="interest in interests" :key="interest.value" class="interest-option">
            <input
              type="checkbox"
              v-model="selectedInterests"
              :value="interest.value"
            />
            <span class="interest-label">
              {{ interest.label }}
              <span class="emoji">{{ interest.emoji }}</span>
            </span>
          </label>
        </div>
      </div>

      <div class="form-section">
        <h3>When would you prefer to explore the city?</h3>
        <div class="time-inputs">
          <div class="time-field">
            <label>Preferred Start Time</label>
            <input type="time" v-model="preferredStartTime" required />
          </div>
          <div class="time-field">
            <label>Preferred End Time</label>
            <input type="time" v-model="preferredEndTime" required />
          </div>
        </div>
      </div>

      <div class="form-section">
        <h3>How active do you want your free time to be?</h3>
        <div class="pace-slider">
          <input
            type="range"
            v-model="selectedPace"
            min="0"
            max="2"
            step="1"
          />
          <div class="pace-labels">
            <span>Relaxed</span>
            <span>Moderate</span>
            <span>Active</span>
          </div>
        </div>
      </div>

      <button type="submit" class="submit-button">
        Start helping me!
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import type { UserPreferences } from '../types';

const occupationOptions = [
  { value: 'student', label: 'Student', emoji: '📚' },
  { value: 'worker', label: 'Worker', emoji: '💼' },
  { value: 'other', label: 'Other', emoji: '✨' }
];

const interests = [
  { value: 'culture', label: 'Culture', emoji: '🏛️' },
  { value: 'food', label: 'Food', emoji: '🍽️' },
  { value: 'nature', label: 'Nature', emoji: '🌳' },
  { value: 'shopping', label: 'Shopping', emoji: '🛍️' },
  { value: 'entertainment', label: 'Entertainment', emoji: '🎭' }
];

const paceMap = ['relaxed', 'moderate', 'active'] as const;

const selectedOccupation = ref<UserPreferences['occupation']>('student');
const schedule = reactive({
  workStartTime: '09:00',
  workEndTime: '17:00',
  breakTime: '12:00',
  breakDuration: 60
});
const selectedInterests = ref<string[]>([]);
const preferredStartTime = ref('18:00');
const preferredEndTime = ref('21:00');
const selectedPace = ref(1);

const emit = defineEmits<{
  (e: 'submit', preferences: UserPreferences): void
}>();

const submitPreferences = () => {
  const preferences: UserPreferences = {
    occupation: selectedOccupation.value,
    schedule: {
      workStartTime: schedule.workStartTime,
      workEndTime: schedule.workEndTime,
      breakTime: schedule.breakTime,
      breakDuration: schedule.breakDuration
    },
    interests: selectedInterests.value,
    pace: paceMap[selectedPace.value],
    preferredStartTime: preferredStartTime.value,
    preferredEndTime: preferredEndTime.value
  };
  emit('submit', preferences);
};
</script>

<style scoped>
.preferences-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.form-section {
  margin-bottom: 2rem;
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

h3 {
  color: #444;
  margin-bottom: 1rem;
}

.occupation-section {
  padding: 2rem;
}

.occupation-section h3 {
  font-size: 1.75rem;
  font-weight: 500;
  margin-bottom: 1.5rem;
}

.occupation-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 400px;
  margin: 0 auto;
}

.occupation-card {
  position: relative;
  display: block;
  padding: 1.5rem;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.occupation-card:hover {
  border-color: #D1D5DB;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.occupation-card.selected {
  border: 2px solid #3B82F6;
  background-color: #F8FAFC;
}

.radio-input {
  position: absolute;
  left: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid #D1D5DB;
  border-radius: 50%;
  appearance: none;
  -webkit-appearance: none;
  transition: all 0.2s ease;
}

.radio-input:checked {
  border-color: #3B82F6;
  background-color: #3B82F6;
  box-shadow: inset 0 0 0 3px white;
}

.occupation-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-left: 3rem;
}

.occupation-title {
  font-size: 1.25rem;
  color: #1F2937;
  font-weight: 500;
}

.occupation-emoji {
  font-size: 1.5rem;
}

.schedule-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.interests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.interest-option {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.interest-option:hover {
  border-color: #666;
}

.interest-label {
  display: flex;
  justify-content: space-between;
  width: 100%;
  align-items: center;
  padding-left: 1rem;
}

.emoji {
  font-size: 1.2rem;
  transition: transform 0.2s;
}

.time-inputs {
  display: flex;
  gap: 2rem;
}

.time-field {
  flex: 1;
}

.time-field label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

.time-field input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.time-field input[type="number"] {
  height: 38px;
}

.pace-slider {
  width: 100%;
  padding: 0 1rem;
}

.pace-slider input {
  width: 100%;
  margin: 1rem 0;
}

.pace-labels {
  display: flex;
  justify-content: space-between;
  color: #666;
}

.submit-button {
  width: 100%;
  padding: 1rem;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 2rem;
}

.submit-button:hover {
  background-color: #444;
  transform: translateY(-2px);
}

.submit-button:active {
  transform: translateY(0);
}

@media (max-width: 600px) {
  .occupation-section {
    padding: 1.5rem;
  }
  
  .occupation-section h3 {
    font-size: 1.5rem;
  }
  
  .occupation-card {
    padding: 1.25rem;
  }
  
  .schedule-grid {
    grid-template-columns: 1fr;
  }
  
  .time-inputs {
    flex-direction: column;
  }
}
</style> 