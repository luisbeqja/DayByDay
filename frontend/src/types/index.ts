export interface Activity {
  id: string;
  name: string;
  description: string;
  location: string;
  category: 'food' | 'culture' | 'nature' | 'shopping' | 'entertainment';
  duration: number; // in minutes
  price: number;
  imageUrl: string;
  rating: number;
  timeOfDay: 'morning' | 'afternoon' | 'evening' | 'any';
}

export interface UserPreferences {
  occupation: 'student' | 'worker' | 'other';
  schedule: {
    workStartTime: string;
    workEndTime: string;
    breakTime: string;
    breakDuration: number; // in minutes
  };
  interests: string[];
  pace: 'relaxed' | 'moderate' | 'active';
  preferredStartTime: string;
  preferredEndTime: string;
} 