<template>
    <nav class="navbar navbar-expand-lg bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand fs-3 fw-bold" href="#">News 55:</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
                <li class = "nav-item">
                    <router-link class="nav-link text-light" :to="{ name: 'Main Page' }">Main Page</router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link text-light" :to="{ name: 'Favourite Page' }">Favourite Page</router-link>
                </li>
                <li class = "nav-item">
                    <router-link class="nav-link text-light" :to="{ name: 'Profile Page' }">Profile Page</router-link>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/accounts/logout/">Logout</a>
                </li>
            </div>
            </div>
        </div>
    </nav>


  <main class="container pt-4">
  <RouterView class="flex-shrink-0" />
  </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";
import { storeMe } from './storage/userDetails';

export default defineComponent({
  components: { RouterView },
  mounted() {
    this.saveDetails();
    this.updateCsrfToken();
  },
  methods: {
    async saveDetails() {
        const profileResponse = await fetch("http://127.0.0.1:8000/get-profile/");
        const favouritesResponse = await fetch("http://127.0.0.1:8000/get-favourites/");

        const profileData = await profileResponse.json();
        const favouritesData = await favouritesResponse.json();

        const favouriteCategory = favouritesData['favourite_categories'];
        
        const store = storeMe();
        const userDataWithCategories = { ...profileData, categories: favouriteCategory };
        store.setCurrentUser(userDataWithCategories);
    },

    updateCsrfToken() {
      const csrfToken = this.getCsrfToken();
      if (csrfToken) {
        const store = storeMe();
        store.setCsrfToken(csrfToken);
      }
    },
    getCsrfToken() {
      const csrfTokenCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
      return csrfTokenCookie.split('=')[1];
    },
  }
});
</script>

<style scoped>
</style>