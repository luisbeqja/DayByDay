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
      <div class="text-content">
        <h1 class="typing-text">{{ displayedText.title }}</h1>
        <p class="typing-text">{{ displayedText.subtitle }}</p>
        
        <p class="description typing-text">
          {{ displayedText.description }}
        </p>
        
        <p class="prompt typing-text">
          {{ displayedText.prompt }}
        </p>
        
        <p class="tagline typing-text">
          {{ displayedText.tagline }}
        </p>
      </div>
      
      <div class="button-container">
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

defineEmits(['start']);

const isSphereAnimated = ref(false);
const isAudioPlaying = ref(false);
const isAudioAlreadyPlayed = ref(false);
const audio = ref<HTMLAudioElement | null>(null);

// Full text content
const fullText = {
  title: "Hey, I'm Anty",
  subtitle: "your personal daily planner for the magical city of Antwerp! ✨",
  description: "Whether you're tired of visiting the same old spots or you're eager to discover hidden gems around the city, I'm here to craft a unique journey for you, one day at a time.",
  prompt: "But first tell me a bit about your typical day, and I'll take care of the rest.",
  tagline: "Let's make your everyday... a little more interesting. 🚲✨"
};

// Displayed text (will be updated character by character)
const displayedText = ref({
  title: "",
  subtitle: "",
  description: "",
  prompt: "",
  tagline: ""
});

// Typing animation control
const typeSpeed = 50; // milliseconds per character

const typeText = async (text: string, target: keyof typeof displayedText.value): Promise<void> => {
  return new Promise((resolve) => {
    let currentIndex = 0;
    const interval = setInterval(() => {
      if (currentIndex <= text.length) {
        displayedText.value[target] = text.slice(0, currentIndex);
        currentIndex++;
      } else {
        clearInterval(interval);
        resolve();
      }
    }, typeSpeed);
  });
};

const startTypingAnimation = async () => {
  // Reset all text
  Object.keys(displayedText.value).forEach(key => {
    displayedText.value[key as keyof typeof displayedText.value] = "";
  });

  // Type each section with delays
  await typeText(fullText.title, "title");
  await new Promise(resolve => setTimeout(resolve, 500));
  
  await typeText(fullText.subtitle, "subtitle");
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  await typeText(fullText.description, "description");
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  await typeText(fullText.prompt, "prompt");
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  await typeText(fullText.tagline, "tagline");
};

const playWelcomeAudio = async () => {
  try {
    if (!audio.value) {
      console.log("Playing welcome audio");
      audio.value = new Audio('http://localhost:5000/api/welcome-audio');
      audio.value.addEventListener('play', () => {
        console.log("Audio playing");
        isAudioPlaying.value = true;
        isSphereAnimated.value = true;
        startTypingAnimation();
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
      // Reset text when audio is paused
      Object.keys(displayedText.value).forEach(key => {
        displayedText.value[key as keyof typeof displayedText.value] = "";
      });
    }
  } catch (error) {
    console.error('Error playing audio:', error);
  }
};
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
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  min-height: 70vh;
  position: relative;
  display: flex;
  flex-direction: column;
}

.text-content {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 1rem;
  text-align: left;
  padding: 0 1rem;
}

.button-container {
  position: sticky;
  bottom: 0;
  padding-top: 1rem;
  background-color: rgba(255, 255, 255, 0.9);
  text-align: center;
}

.text-section {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.text-section.show {
  opacity: 1;
  transform: translateY(0);
}

h1.typing-text {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 0.5rem;
  text-align: center;
}

p.typing-text {
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
  text-align: center;
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

.typing-text {
  white-space: pre-wrap;
  word-break: break-word;
  min-height: 1.2em;
  position: relative;
  overflow: hidden;
}
</style> 