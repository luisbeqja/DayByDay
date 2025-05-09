import type { Activity } from '../types';

export const mockActivities: Activity[] = [
  {
    id: '1',
    name: 'Visit MAS Museum',
    description: 'Explore the iconic MAS Museum with panoramic city views and fascinating exhibitions about Antwerp\'s history and culture.',
    location: 'Hanzestedenplaats 1, 2000 Antwerp',
    category: 'culture',
    duration: 180,
    price: 12,
    imageUrl: '/images/mas-museum.jpg',
    rating: 4.6,
    timeOfDay: 'any'
  },
  {
    id: '2',
    name: 'Lunch at Grote Markt',
    description: 'Enjoy traditional Belgian cuisine at one of the historic restaurants in Antwerp\'s main square.',
    location: 'Grote Markt, 2000 Antwerp',
    category: 'food',
    duration: 90,
    price: 25,
    imageUrl: '/images/grote-markt.jpg',
    rating: 4.4,
    timeOfDay: 'afternoon'
  },
  {
    id: '3',
    name: 'Antwerp Zoo Visit',
    description: 'One of the oldest and most beautiful zoos in the world, home to over 5000 animals.',
    location: 'Koningin Astridplein 20-26, 2018 Antwerp',
    category: 'entertainment',
    duration: 240,
    price: 29,
    imageUrl: '/images/zoo.jpg',
    rating: 4.7,
    timeOfDay: 'morning'
  },
  {
    id: '4',
    name: 'Shopping at Meir',
    description: 'Shop at Antwerp\'s main shopping street featuring international brands and local boutiques.',
    location: 'Meir, 2000 Antwerp',
    category: 'shopping',
    duration: 180,
    price: 0,
    imageUrl: '/images/meir.jpg',
    rating: 4.3,
    timeOfDay: 'any'
  },
  {
    id: '5',
    name: 'Sunset at Scheldt River',
    description: 'Take a peaceful walk along the river and enjoy the beautiful sunset views.',
    location: 'Sint-Andries, 2000 Antwerp',
    category: 'nature',
    duration: 60,
    price: 0,
    imageUrl: '/images/scheldt-river.jpg',
    rating: 4.8,
    timeOfDay: 'evening'
  }
]; 