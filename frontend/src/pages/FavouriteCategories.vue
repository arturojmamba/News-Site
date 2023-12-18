<template>
    <div class="container my-4">
      <h1 class="display-4 mb-4 text-center">{{ title }}</h1>
      <div v-for="category in categories" :key="category.id" class="mb-5">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-primary text-white">
            <h2 class="h5 mb-0">{{ category.name }}</h2>
          </div>
          <ul class="list-group list-group-flush">
            <li v-for="article in category.articles" :key="article.id" class="list-group-item d-flex justify-content-between align-items-center">
              <router-link :to="{ name: 'Article Page', params: { id: parseInt(article.id, 10) } }" class="text-decoration-none stretched-link">
                <h5 class="mb-0">{{ article.title }}</h5>
              </router-link>
            </li>
            <li v-if="category.articles.length === 0" class="list-group-item">
              <span class="text-muted">No articles available.</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";

  export default defineComponent({
    data() {
        return {
            title: "Favourites",
            articles: [] as any[],
            categories: [] as any[], 
        }
    },
    mounted() {
      this.fetchCategories();
    },
    methods: {
      fetchCategories() {
        fetch('http://127.0.0.1:8000/get-favourites/')
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          })
          .then(data => {
            this.categories = data.favourite_categories;
            return Promise.all(
              this.categories.map(category => 
                fetch(`http://127.0.0.1:8000/categories/${category.id}/articles/`)
                  .then(response => {
                    if (!response.ok) {
                      throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                  })
                  .then(articleData => {

                    category.articles = articleData.articles;
                  })
              )
            );
          })
          .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
          });
      }
    }
  })
</script>
  

  
  <style scoped>
  </style>