<script setup lang="ts">
import { useRouter } from 'vue-router';
import WelcomeScreen from '../components/WelcomeScreen.vue';

const router = useRouter();

const handleStart = () => {
  router.push('/preferences');
};
</script>

<template>
  <WelcomeScreen @start="handleStart" />
</template>

<style scoped>
.header {
  text-align: center;
  padding: 30px 0;
  background-color: #f8f9fa;
  margin-bottom: 20px;
}

h1 {
  margin-bottom: 10px;
  color: #343a40;
}

p {
  color: #6c757d;
  margin-bottom: 20px;
}

.start-button {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 1rem 2rem;
  font-size: 1.2rem;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.start-button:hover {
  background: #45a049;
  transform: translateY(-2px);
}

main {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
</style>
