// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/MainPage.vue';
import FavouritePage from '../pages/FavouriteCategories.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import ArticlePage from '../pages/ArticlePage.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Main Page', component: MainPage },
        { path: '/favourite/', name: 'Favourite Page', component: FavouritePage },
        { path: '/profile/', name: 'Profile Page', component: ProfilePage },
        { path: '/article/:id', name: 'Article Page', component: ArticlePage, props: route => ({ id: Number(route.params.id) }) },
    ]
})

export default router
