<template>
    <button @click="getCsrfToken" class="btn btn-secondary" data-bs-toggle="modal" data-bs-target="#editCategories">Update Favorite Categories</button>
    
    <div class="modal fade" id="editCategories" tabindex="-1" aria-labelledby="editCategoriesLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="editCategoriesLabel">Update Favorite Categories</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <form @submit="catUpdated">
                      <div>
                      <div v-for="(cat, index) in cats" :key="cat.id" class="form-check">
                      <input :id="'checkbox' + cat.id" class="form-check-input" type="checkbox" :value="cat.id" :name="'checkbox' + cat.id" v-model="selectedCategories"/>
                      <label :for="'checkbox' + cat.id" class="form-check-label">{{ cat.name }}</label>
                      </div>
                      </div>
                      <p></p>
                       <button type="submit" class="btn btn-primary">Save Changes</button>
                  </form>
                </div>
            </div>
        </div>
    </div>
  </template>
  
  
  <script lang="ts"> 
  import { defineComponent, ref } from "vue";
  import { storeMe } from '../storage/userDetails';
  
  export default defineComponent({
      mounted(){
          this.getTheCategories();
      },
      data() {
      return {
        cats: [], 
        selectedCategories: [],
      };
    },
    methods: {
      async getTheCategories(){
          const mycat = await fetch("http://127.0.0.1:8000/get-categories/");
          const data = await mycat.json();
          this.cats = data['categories']
          },
  
      async catUpdated() {
        const categoriesArray: number[] = Object.values(this.selectedCategories);
          const final = {'categories': categoriesArray};
          const csrfTokenCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
        const headers = {'X-CSRFToken': csrfTokenCookie,
          'Content-Type': 'application/json'}
        try {
          const response = await fetch('http://127.0.0.1:8000/update-favourites/', {
            method: 'PUT',
            headers,
            body: JSON.stringify(final),
            credentials: 'include'
          });
  
          if (response.ok) {
            const data = await response.json();
            console.log('Favourite Categories updated:', data.message);
          } else {
            const errorData = await response.json();
            console.error('Error updating favourite categories:', errorData.errors);
          }
        } catch (error) {
          console.error('Fetch error:', error);
        }
  
    },
  
    },
  });
  </script>
  
  <style scoped>
  </style>