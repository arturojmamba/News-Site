<template>
    <div class="container my-4">
      <!-- Article Container -->
      <div class="article-container card mb-5">
        <div class="card-body">
          <h1 class="card-title display-4">{{ article.title }}</h1>
          <p class="card-subtitle mb-2 text-muted" v-if="article.category_name">Category: {{ article.category_name }}</p>
          <p class="card-subtitle mb-2 text-muted" v-if="article.author_email">Author: {{ article.author_email }}</p>
          <p class="card-text mt-4">{{ article.content }}</p>
        </div>
        <div class="card-footer text-muted">Published on: {{ formatDate(article.published) }}</div>
      </div>
  
      <!-- Comments Section -->
      <div class="comments-container">
        <Comments :articleId="id" :csrfToken="csrfToken" @commentAdded="" />
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, onMounted, ref, toRefs } from 'vue';
  import Comments from './Comments.vue';
  import { storeMe } from '../storage/userDetails';
  
  export default defineComponent({
    components: {
      Comments
    },
    props: {
      id: {
        type: Number,
        required: true,
      },
    },
    setup(props) {
      const { id } = toRefs(props);
      const userStore = storeMe();
      const user = userStore.getCurrentUser;
      const csrfToken = user?.csrf_token;
      const article = ref({});
  
      const fetchArticle = async () => {
        try {
          const response = await fetch(`http://127.0.0.1:8000/articles/${id.value}/`);
          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
          article.value = await response.json();
        } catch (error) {
          console.error('Error fetching article:', error);
        }
      };
  
      onMounted(() => {
        fetchArticle();
      });
  
      return { article, id, csrfToken };
    },
    methods: {
      formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
      },
    },
  });
  </script>
  