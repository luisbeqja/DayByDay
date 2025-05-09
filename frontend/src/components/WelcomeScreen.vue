<template>
  <div class="welcome-screen">
    <div class="logo">
      <div class="bubble" @click="playWelcomeAudio">
        <Transition name="fade" mode="out-in">
          <img 
            :key="isSphereAnimated ? 'animated' : 'static'"
            :src="isSphereAnimated ? '/images/ai_sphere_animated.gif' : '/images/ai_sphere.gif'" 
            alt="AI Assistant Sphere" 
            class="sphere-gif"
          />
        </Transition>
      </div>
    </div>
    <div class="message-box">
      <h1>Hey, I'm Anty</h1>
      <p>your personal daily planner for the magical city of Antwerp! ✨</p>
      
      <p class="description">
        Whether you're tired of visiting the same old spots or you're eager to discover hidden gems
        around the city, I'm here to craft a unique journey for you, one day at a time.
      </p>
      
      <p class="prompt">
        But first tell me a bit about your typical day, and I'll take care of the rest.
      </p>
      
      <p class="tagline">
        Let's make your everyday... a little more interesting. 🚲✨
      </p>
      
      <button 
        class="confirm-button" 
        @click="$emit('start')"
        :disabled="isAudioPlaying || !isAudioAlreadyPlayed"
        :class="{ 'disabled': isAudioPlaying || !isAudioAlreadyPlayed }"
      >
        {{ !isAudioAlreadyPlayed ? 'Click the bubble to hear Anty first!' : 
           isAudioPlaying ? 'Please listen to Anty...' : 
           'Start helping me!' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

defineEmits(['start']);

const isSphereAnimated = ref(false);
const isAudioPlaying = ref(false);
const isAudioAlreadyPlayed = ref(false);
const audio = ref<HTMLAudioElement | null>(null);

const toggleAnimation = () => {
  isSphereAnimated.value = !isSphereAnimated.value;
};

const playWelcomeAudio = async () => {
  try {
    if (!audio.value) {
      audio.value = new Audio('/api/welcome-audio');
      audio.value.addEventListener('play', () => {
        isAudioPlaying.value = true;
        isSphereAnimated.value = true;
      });
      audio.value.addEventListener('pause', () => {
        isAudioPlaying.value = false;
        isSphereAnimated.value = false;
      });
      audio.value.addEventListener('ended', () => {
        isAudioPlaying.value = false;
        isSphereAnimated.value = false;
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

onMounted(() => {
  // Initialize audio without auto-playing
  audio.value = new Audio('/api/welcome-audio');
  audio.value.addEventListener('play', () => {
    isAudioPlaying.value = true;
    isSphereAnimated.value = true;
  });
  audio.value.addEventListener('pause', () => {
    isAudioPlaying.value = false;
    isSphereAnimated.value = false;
  });
  audio.value.addEventListener('ended', () => {
    isAudioPlaying.value = false;
    isSphereAnimated.value = false;
    isAudioAlreadyPlayed.value = true;
  });
});
</script>

<style scoped>
.welcome-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  max-width: 600px;
  margin: 0 auto;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.logo {
  margin-bottom: 2rem;
}

.bubble {
  width: 160px;
  height: 160px;
  background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(255,255,255,0.4));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  overflow: hidden;
  cursor: pointer;
  position: relative;
}

.bubble:hover {
  transform: scale(1.05);
}

.bubble:active {
  transform: scale(0.95);
}

.sphere-gif {
  height: 700px;
  object-fit: cover;
  border-radius: 50%;
  will-change: opacity, transform;
}

.message-box {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 2rem;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

h1 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 0.5rem;
}

p {
  margin: 1rem 0;
  line-height: 1.6;
  color: #666;
}

.description {
  margin: 2rem 0;
}

.prompt {
  font-weight: 500;
  color: #444;
}

.tagline {
  font-style: italic;
  margin-top: 2rem;
}

.confirm-button {
  margin-top: 2rem;
  padding: 0.8rem 2rem;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s, background-color 0.2s, opacity 0.2s;
}

.confirm-button:not(.disabled):hover {
  transform: translateY(-2px);
  background-color: #444;
}

.confirm-button:not(.disabled):active {
  transform: translateY(0);
}

.confirm-button.disabled {
  background-color: #999;
  cursor: not-allowed;
  transform: none;
  opacity: 0.7;
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  transform: scale(1);
}
</style> 