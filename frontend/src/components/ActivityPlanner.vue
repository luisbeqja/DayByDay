<template>
    <p class="typing-text">{{ activityDetailsText }}</p>
    
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const currentActivity = ref<string | null>(null);
const activityDetails = ref<string | null>(null);
const activityDetailsText = ref<string | null>(null);
const fetchActivity = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/agent/get-activity');
    const data = await response.json();
    
    if (data.activity) {
      currentActivity.value = data.activity;
      activityDetails.value = data.details || null;
      activityDetailsText.value = JSON.parse(data.details).text_to_speech || null;
    }
    console.log(activityDetailsText);
  } catch (error) {
    console.error('Error fetching activity:', error);
  }
};

onMounted(() => {
  fetchActivity();
});

// Expose methods to parent component
defineExpose({
  fetchActivity
});
</script>

<style scoped>
.activity-planner {
  padding: 1rem;
}

.activity-details {
  margin-top: 1rem;
  padding: 1rem;
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

.loading {
  text-align: center;
  margin-top: 2rem;
  color: #666;
}

.typing-text {
  white-space: pre-wrap;
  word-break: break-word;
  min-height: 1.2em;
  position: relative;
  overflow: hidden;
}
</style> 