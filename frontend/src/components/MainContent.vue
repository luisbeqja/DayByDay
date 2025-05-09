<template>
  <div class="main-content">
    <h2>Welcome to Your Vue PWA</h2>
    <div class="content">
      <p>This is a clean boilerplate for building Progressive Web Apps with:</p>
      <ul>
        <li>Vue 3 + TypeScript</li>
        <li>Vite build tool</li>
        <li>PWA capabilities</li>
        <li>Python Flask backend</li>
      </ul>
      <div class="action-buttons">
        <button class="button primary" @click="checkApiStatus">Check API Status</button>
        <button class="button secondary" @click="requestNotificationPermission">{{ notificationBtnText }}</button>
      </div>
      <div v-if="apiStatus" class="status-box" :class="{ success: apiStatus.status === 'ok' }">
        <p>{{ apiStatus.message }}</p>
      </div>
      <div v-if="notificationMessage" class="status-box" :class="{ success: notificationStatus }">
        <p>{{ notificationMessage }}</p>
      </div>
      <div v-if="showSendNotification" class="notification-demo">
        <h3>Notification Demo</h3>
        <div class="tabs">
          <button 
            class="tab-button" 
            :class="{ active: activeTab === 'local' }" 
            @click="activeTab = 'local'"
          >
            Local Notification
          </button>
          <button 
            class="tab-button" 
            :class="{ active: activeTab === 'push' }" 
            @click="activeTab = 'push'"
          >
            Push Notification
          </button>
        </div>
        
        <div class="tab-content">
          <div class="form-group">
            <label for="notificationTitle">Title</label>
            <input id="notificationTitle" v-model="testNotification.title" type="text" placeholder="Notification Title">
          </div>
          <div class="form-group">
            <label for="notificationBody">Message</label>
            <input id="notificationBody" v-model="testNotification.body" type="text" placeholder="Notification Message">
          </div>
          <div v-if="activeTab === 'push'" class="form-group">
            <label for="notificationUrl">URL (optional)</label>
            <input id="notificationUrl" v-model="testNotification.url" type="text" placeholder="https://example.com">
          </div>
          <button 
            class="button primary" 
            @click="activeTab === 'local' ? sendTestNotification() : sendPushNotification()"
          >
            Send {{ activeTab === 'local' ? 'Local' : 'Push' }} Notification
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { NotificationService } from '@/services/NotificationService'

const apiStatus = ref<{ status: string; message: string } | null>(null)
const notificationService = new NotificationService()
const notificationStatus = ref(false)
const notificationMessage = ref('')
const notificationPermission = ref<NotificationPermission>('default')
const showSendNotification = ref(false)
const activeTab = ref<'local' | 'push'>('local')
const testNotification = ref({
  title: 'Test Notification',
  body: 'This is a test notification from your PWA',
  url: '/'
})

onMounted(async () => {
  await checkNotificationSupport()
  
  // Check if permission is already granted
  if ('Notification' in window) {
    notificationPermission.value = Notification.permission
    if (notificationPermission.value === 'granted') {
      showSendNotification.value = true
    }
  }
})

const notificationBtnText = computed(() => {
  switch (notificationPermission.value) {
    case 'granted':
      return 'Notifications Enabled'
    case 'denied':
      return 'Notifications Blocked'
    default:
      return 'Enable Notifications'
  }
})

const checkApiStatus = async () => {
  try {
    const response = await fetch('/api/health')
    if (!response.ok) {
      throw new Error('API request failed')
    }
    apiStatus.value = await response.json()
  } catch (error) {
    apiStatus.value = {
      status: 'error',
      message: 'Failed to connect to API'
    }
  }
}

const checkNotificationSupport = async () => {
  const isSupported = await notificationService.checkNotificationSupport()
  notificationStatus.value = isSupported
  if (!isSupported) {
    notificationMessage.value = 'Push notifications are not supported in this browser'
  }
  return isSupported
}

const requestNotificationPermission = async () => {
  try {
    // If already granted or denied, don't ask again
    if (notificationPermission.value !== 'default') {
      notificationMessage.value = notificationPermission.value === 'granted' 
        ? 'Notification permission already granted'
        : 'Notification permission was denied. Please enable in browser settings.'
      return
    }
    
    const permission = await notificationService.requestPermission()
    notificationPermission.value = permission
    
    if (permission === 'granted') {
      notificationMessage.value = 'Notification permission granted!'
      notificationStatus.value = true
      showSendNotification.value = true
      // Subscribe to push notifications
      const subscription = await notificationService.subscribeToPush()
      if (subscription) {
        console.log('Successfully subscribed to push notifications')
      }
    } else {
      notificationMessage.value = 'Notification permission denied'
      notificationStatus.value = false
    }
  } catch (error) {
    notificationMessage.value = `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
    notificationStatus.value = false
  }
}

const sendTestNotification = async () => {
  try {
    if (notificationPermission.value !== 'granted') {
      notificationMessage.value = 'You need to grant notification permission first'
      return
    }
    
    const success = await notificationService.showNotification(
      testNotification.value.title,
      {
        body: testNotification.value.body,
        icon: '/pwa-192x192.png',
        badge: '/pwa-192x192.png'
      }
    )
    
    if (success) {
      notificationMessage.value = 'Local notification sent!'
      notificationStatus.value = true
    } else {
      throw new Error('Failed to send notification')
    }
  } catch (error) {
    notificationMessage.value = `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
    notificationStatus.value = false
  }
}

const sendPushNotification = async () => {
  try {
    if (notificationPermission.value !== 'granted') {
      notificationMessage.value = 'You need to grant notification permission first'
      return
    }
    
    const success = await notificationService.sendPushNotification(
      testNotification.value.title,
      testNotification.value.body,
      testNotification.value.url
    )
    
    if (success) {
      notificationMessage.value = 'Push notification sent!'
      notificationStatus.value = true
    } else {
      throw new Error('Failed to send push notification')
    }
  } catch (error) {
    notificationMessage.value = `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
    notificationStatus.value = false
  }
}
</script>

<style scoped>
.main-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #343a40;
}

.content {
  background-color: #f8f9fa;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

ul {
  margin: 15px 0;
  padding-left: 20px;
}

li {
  margin-bottom: 8px;
}

.action-buttons {
  margin: 25px 0;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition:
    background-color 0.2s,
    transform 0.1s;
}

.button:hover {
  transform: translateY(-2px);
}

.button:active {
  transform: translateY(0);
}

.primary {
  background-color: #007bff;
  color: white;
}

.primary:hover {
  background-color: #0069d9;
}

.secondary {
  background-color: #6c757d;
  color: white;
}

.secondary:hover {
  background-color: #5a6268;
}

.status-box {
  margin-top: 20px;
  padding: 15px;
  border-radius: 4px;
  background-color: #f8d7da;
  color: #721c24;
  text-align: center;
}

.status-box.success {
  background-color: #d4edda;
  color: #155724;
}

.notification-demo {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #dee2e6;
}

h3 {
  margin-bottom: 15px;
  text-align: center;
}

.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #dee2e6;
}

.tab-button {
  padding: 8px 16px;
  margin: 0 5px;
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  border-bottom: 3px solid transparent;
}

.tab-button.active {
  border-bottom-color: #007bff;
  color: #007bff;
  font-weight: 600;
}

.tab-content {
  padding-top: 15px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
}

input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 16px;
}
</style>
 