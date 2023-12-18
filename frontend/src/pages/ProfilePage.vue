<template>
  <div class="profile-page">
    <div class="h3">{{ title }}</div>
    <div class="container mt-4 mb-4 p-3 d-flex justify-content-center">
      <div class="card p-4">
        <div class="image d-flex flex-column justify-content-center align-items-center">
          <img :src="pic" height="100" width="100">
          <p></p>
          <span>Email: {{ email }}</span>
          <span>DOB: {{ dob }}</span>
          <span>Favorite News Category: {{categories}}</span>
          <p></p>
          <div class="d-flex mt-3">
            <editProfile />
            <editCategories />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import editProfile from './editProfile.vue';
import editCategories from './editCategories.vue';
import { storeMe } from '../storage/userDetails';

export default defineComponent({
  components: { editProfile, editCategories },
  setup() {
    const userStore = storeMe();
    const user = computed(() => userStore.getCurrentUser);
    return {
      title: "Profile Page",
      email: computed(() => user.value ? user.value.email : ''),
      dob: computed(() => user.value ? user.value.date_of_birth : ''),
      pic: computed(() => user.value && user.value.profile_image ? user.value.profile_image : 'http://127.0.0.1:8000/media/profile_images/default.png/'), // Fallback to a default picture
      categories: computed(() => user.value && user.value.categories ? user.value.categories.map(category => category.name).join(', ') : ''),
    };
  }
});
</script>

<style scoped>
</style>
