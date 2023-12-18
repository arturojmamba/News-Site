<template>
  <button @click="getTheCategories" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editP">Edit Profile Information</button>
  
  <div class="modal fade" id="editP" tabindex="-1" aria-labelledby="editP" aria-hidden="true">
      <div class="modal-dialog">
          <div class="modal-content">
              <div class="modal-header">
                  <h1 class="modal-title fs-5" id="editP">Edit Profile Information</h1>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                  <form @submit="updateTheProfile">
                      <div class="mb-3">
                          <label for="emailInput" class="form-label">Email address</label>
                          <input type="email" class="form-control" id="emailInput" v-model="email">
                      </div>
                      <div class="mb-3">
                          <label for="dobInput" class="form-label">DOB</label>
                          <input type="date" class="form-control" id="dobInput" v-model="dob">
                      </div>
                      <div class="mb-3">
                          <label for="profileImageInput" class="form-label">Profile Picture</label>
                          <input type="file" class="form-control" id="profileImageInput" ref="profileImageInput" accept="image/*">
                      </div>
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
  methods: {
    async getTheCategories() {
      const response = await fetch("http://127.0.0.1:8000/get-categories/");
      const categories = await response.json();
      console.log(categories);
    },
  },
  setup() {
    const userStore = storeMe();
    const user = userStore.getCurrentUser;
    const email = ref(user ? user.email : '');
    const dob = ref(user ? user.date_of_birth : '');
    const profileImageInput = ref(null);
    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];

    const updateTheProfile = async () => {
      const formData = new FormData();
      formData.append('email', email.value);
      formData.append('date_of_birth', dob.value);

      if (profileImageInput.value?.files[0]) {
        formData.append('profile_image', profileImageInput.value.files[0]);
      }

      const headers = csrfToken ? { 'X-CSRFToken': csrfToken } : {};

      try {
        const response = await fetch('http://127.0.0.1:8000/update-profile/', {
          method: 'POST',
          headers,
          body: formData,
          credentials: 'include'
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Profile updated:', data.message);
        } else {
          const errorData = await response.json();
          console.error('Error updating profile:', errorData.errors);
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    };

    return {
      email,
      dob,
      profileImageInput,
      updateTheProfile
    };
  }
});
</script>

<style scoped>
</style>
