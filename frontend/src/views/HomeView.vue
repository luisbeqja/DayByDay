<script setup lang="ts">
import MainContent from '@/components/MainContent.vue'
</script>

<template>
  <main>
    <div class="header">
      <h1>Vue PWA Boilerplate</h1>
      <p>A Progressive Web App built with Vue and Flask</p>
    </div>
    <MainContent />
  </main>
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
}

main {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
</style>
