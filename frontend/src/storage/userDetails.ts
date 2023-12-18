import { defineStore } from 'pinia';

interface User {
  email: string;
  dob: Date;
  profile_pic: string;
  csrf_token: string;
  categories: { id: number; name: string }[];
}

export const storeMe = defineStore('user', {
  state: () => ({
    user_state: JSON.parse(localStorage.getItem('user_state') || 'null') as User | null,
  }),
  actions: {
    setCurrentUser(given_user: User): void {
      this.user_state = given_user;
      localStorage.setItem('user_state', JSON.stringify(given_user));
    },
    logOut(): void {
      this.user_state = null;
      localStorage.removeItem('user_state');
    },
    setCsrfToken(token: string): void {
      this.user_state.csrf_token = token;
      localStorage.setItem('user_state', JSON.stringify(this.user_state));
    }
  },
  getters: {
    getCurrentUser(): User | null {
      return this.user_state;
    },
  },
});