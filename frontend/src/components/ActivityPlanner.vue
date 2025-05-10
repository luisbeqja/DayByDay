<template>
    <div class="activity-planner">
        <div v-if="isLoading" class="loading">
            <div class="loader"></div>
            <p>Loading activity...</p>
        </div>
        <div v-else-if="activityDetails?.activity_name" class="map-container">
          <h3>{{ activityDetails.activity_name.charAt(0).toUpperCase() + activityDetails.activity_name.slice(1) }}</h3>
            <iframe
              width="100%"
              height="450"
              style="border:0"
              loading="lazy"
              allowfullscreen
              referrerpolicy="no-referrer-when-downgrade"
              :src="`https://www.google.com/maps/embed/v1/directions?key=${googleMapsApiKey}&origin=51.2206,4.4024&destination=51.2202934,4.3995386&mode=walking`">
            </iframe>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const currentActivity = ref<string | null>(null);
const activityDetails = ref<any>(null);
const activityDetailsText = ref<string | null>(null);
const isLoading = ref(true);
const isAudioPlaying = ref(false);
const googleMapsApiKey = "AIzaSyApQ_wJx0zPLu2ZunHJGt5xQCHICFJnstw";

const audio = ref<HTMLAudioElement | null>(null);
const isAudioAlreadyPlayed = ref(false);

const emit = defineEmits(['update:sphereAnimated']);

const playAudio = async () => {
  try {
    if (!audio.value) {
      console.log("Playing welcome audio");
      audio.value = new Audio('http://localhost:5000/api/read-text?text=' + activityDetailsText.value);
      audio.value.addEventListener('play', () => {
        console.log("Audio playing");
        isAudioPlaying.value = true;
        emit('update:sphereAnimated', true);
      });
      audio.value.addEventListener('pause', () => {
        isAudioPlaying.value = false;
        emit('update:sphereAnimated', false);
      });
      audio.value.addEventListener('ended', () => {
        isAudioPlaying.value = false;
        emit('update:sphereAnimated', false);
        isAudioAlreadyPlayed.value = true;
      });
    }
    
    if (!isAudioPlaying.value) {
      await audio.value.play();
    } else {
      audio.value.pause();
    }
  } catch (error) {
    console.error('Error playing audio:', error);
  }
};

const fetchActivity = async () => {
  isLoading.value = true;
  try {
    const response = await fetch('http://localhost:5000/api/agent/get-activity');
    const data = await response.json();
    
    if (data.activity) {
      currentActivity.value = data.activity.result;
      activityDetails.value = data.details.result || null;
      activityDetailsText.value = data.details.result.text_to_speech || null;
    }
    console.log('Activity data:', data);
  } catch (error) {
    console.error('Error fetching activity:', error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchActivity();
});

// Expose methods to parent component
defineExpose({
  fetchActivity,
  playAudio
});
</script>

<style scoped>
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
  width: 100%;
}

.loader {
    width: 48px;
    height: 48px;
    border: 5px solid #FFF;
    border-bottom-color: #FF3D00;
    border-radius: 50%;
    display: inline-block;
    box-sizing: border-box;
    animation: rotation 1s linear infinite;
    margin-bottom: 1rem;
}

@keyframes rotation {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}

.loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    text-align: center;
    color: #666;
}

.map-container {
    border-radius: 16px;
    overflow: hidden;
    background: white;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    padding-top: 1rem;
}

.map-container:hover {
    transform: translateY(-2px);
}

.map-container iframe {
    display: block;
    border-radius: 16px;
    width: 100%;
    height: 450px;
    background: #f5f5f5;
}
</style> 