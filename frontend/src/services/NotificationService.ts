/**
 * NotificationService.ts
 * Handles browser notifications and push subscription
 */

export class NotificationService {
  private swRegistration: ServiceWorkerRegistration | null = null;
  private vapidPublicKey: string | null = null;

  // Check if the browser supports notifications
  public async checkNotificationSupport(): Promise<boolean> {
    if (!('Notification' in window)) {
      console.log('This browser does not support notifications');
      return false;
    }
    
    if (!('serviceWorker' in navigator)) {
      console.log('This browser does not support service workers');
      return false;
    }
    
    if (!('PushManager' in window)) {
      console.log('This browser does not support push notifications');
      return false;
    }
    
    return true;
  }
  
  // Request notification permission
  public async requestPermission(): Promise<NotificationPermission> {
    if (!await this.checkNotificationSupport()) {
      throw new Error('Notifications not supported');
    }
    
    const permission = await Notification.requestPermission();
    return permission;
  }
  
  // Register service worker
  public async registerServiceWorker(): Promise<ServiceWorkerRegistration | null> {
    try {
      if (!('serviceWorker' in navigator)) {
        throw new Error('Service Worker not supported');
      }
      
      this.swRegistration = await navigator.serviceWorker.register('/sw.js');
      return this.swRegistration;
    } catch (error) {
      console.error('Service Worker registration failed:', error);
      return null;
    }
  }
  
  // Get VAPID public key from server
  public async getVapidPublicKey(): Promise<string> {
    if (this.vapidPublicKey) {
      return this.vapidPublicKey;
    }
    
    try {
      const response = await fetch('/api/vapid-public-key');
      if (!response.ok) {
        throw new Error('Failed to fetch VAPID public key');
      }
      
      const data = await response.json();
      this.vapidPublicKey = data.publicKey;
      
      if (!this.vapidPublicKey) {
        throw new Error('Invalid VAPID public key');
      }
      
      return this.vapidPublicKey;
    } catch (error) {
      console.error('Error fetching VAPID public key:', error);
      throw error;
    }
  }
  
  // Subscribe to push notifications
  public async subscribeToPush(): Promise<PushSubscription | null> {
    try {
      if (!this.swRegistration) {
        this.swRegistration = await this.registerServiceWorker();
        
        if (!this.swRegistration) {
          throw new Error('Service Worker registration failed');
        }
      }
      
      const permission = await this.requestPermission();
      if (permission !== 'granted') {
        throw new Error('Notification permission denied');
      }
      
      // Check if already subscribed
      const existingSubscription = await this.swRegistration.pushManager.getSubscription();
      if (existingSubscription) {
        return existingSubscription;
      }
      
      // Get VAPID public key
      const publicKey = await this.getVapidPublicKey();
      
      // Subscribe the user
      const subscription = await this.swRegistration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: this.urlBase64ToUint8Array(publicKey)
      });
      
      // Send the subscription to the server
      await this.sendSubscriptionToServer(subscription);
      
      return subscription;
    } catch (error) {
      console.error('Error subscribing to push notifications:', error);
      return null;
    }
  }
  
  // Unsubscribe from push notifications
  public async unsubscribeFromPush(): Promise<boolean> {
    try {
      if (!this.swRegistration) {
        const registration = await navigator.serviceWorker.getRegistration();
        if (!registration) {
          throw new Error('No service worker registration found');
        }
        this.swRegistration = registration;
      }
      
      const subscription = await this.swRegistration.pushManager.getSubscription();
      if (!subscription) {
        return true; // Already unsubscribed
      }
      
      // Unsubscribe from push
      const success = await subscription.unsubscribe();
      
      // Notify server about unsubscription
      if (success) {
        await this.removeSubscriptionFromServer(subscription);
      }
      
      return success;
    } catch (error) {
      console.error('Error unsubscribing from push:', error);
      return false;
    }
  }
  
  // Display a notification
  public async showNotification(title: string, options: NotificationOptions = {}): Promise<boolean> {
    try {
      if (!this.swRegistration) {
        const registration = await navigator.serviceWorker.getRegistration();
        if (!registration) {
          throw new Error('No service worker registration found');
        }
        this.swRegistration = registration;
      }
      
      await this.swRegistration.showNotification(title, options);
      return true;
    } catch (error) {
      console.error('Error showing notification:', error);
      return false;
    }
  }
  
  // Send a push notification through the server
  public async sendPushNotification(
    title: string, 
    body: string, 
    url: string = '/'
  ): Promise<boolean> {
    try {
      const response = await fetch('/api/notifications/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title,
          body,
          url
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to send push notification');
      }
      
      const result = await response.json();
      return result.success;
    } catch (error) {
      console.error('Error sending push notification:', error);
      return false;
    }
  }
  
  // Convert base64 to Uint8Array for applicationServerKey
  private urlBase64ToUint8Array(base64String: string): Uint8Array {
    const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, '+')
      .replace(/_/g, '/');
    
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    
    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    
    return outputArray;
  }
  
  // Send the subscription to the server
  private async sendSubscriptionToServer(subscription: PushSubscription): Promise<void> {
    try {
      const response = await fetch('/api/notifications/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ subscription }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to store subscription on server');
      }
    } catch (error) {
      console.error('Error saving push subscription:', error);
      throw error;
    }
  }
  
  // Remove the subscription from the server
  private async removeSubscriptionFromServer(subscription: PushSubscription): Promise<void> {
    try {
      const response = await fetch('/api/notifications/unsubscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ subscription }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to remove subscription from server');
      }
    } catch (error) {
      console.error('Error removing push subscription:', error);
      throw error;
    }
  }
} 