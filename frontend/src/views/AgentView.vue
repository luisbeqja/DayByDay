<template>
  <div class="welcome-screen">
    <div class="logo">
      <div class="bubble">
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
        <ActivityPlanner ref="activityPlannerRef" />
      </div>
      
      <div class="button-container">
        <button 
          class="confirm-button" 
          @click="handleContinue"
        >
          Next Activity
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ActivityPlanner from '../components/ActivityPlanner.vue';

const router = useRouter();
const isSphereAnimated = ref(false);
const activityPlannerRef = ref<InstanceType<typeof ActivityPlanner> | null>(null);

const handleContinue = async () => {
  if (activityPlannerRef.value) {
    await activityPlannerRef.value.fetchActivity();
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
  width: 100%;
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