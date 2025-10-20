<template>
  <div>
    <div v-if="isAuthed" class="flex items-center gap-3">
      <div class="font-mono text-sm">{{ user?.username || ('id ' + user?.telegram_id) }}</div>
      <button @click="logout" class="font-mono text-accent-400 hover:text-accent-300 text-sm">Logout</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '../stores/auth'

const auth = useAuth()
const isAuthed = auth.isAuthenticated
const user = auth.user

async function logout() {
  await auth.logout()
}
</script>


