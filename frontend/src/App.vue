<template>
  <div class="min-h-full flex flex-col">
    <header v-if="isAuthed" class="px-5 py-4 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="text-2xl font-semibold tracking-wide font-mono">Telepad</div>
        <div class="text-sm text-accent-400 font-mono">@tlpadbot</div>
      </div>
      <LoginOrUser />
    </header>
    <main class="flex-1 px-4 pb-6">
      <div class="max-w-3xl mx-auto">
        <template v-if="isAuthed">
          <Toggle v-model="mode" />
          <Board :mode="mode" />
        </template>
        <template v-else>
          <div class="h-[70vh] grid place-items-center">
            <div class="flex flex-col items-center gap-6 w-full">
              <div class="font-bold font-mono text-[10vw] leading-tight max-w-[50vw] text-center">Telepad</div>
              <div class="text-accent-400 text-sm">The Telegram-integrated soundboard.</div>
              <TelegramLogin />
            </div>
          </div>
        </template>
      </div>
    </main>
  </div>
  
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import Toggle from './components/Toggle.vue'
import Board from './components/Board.vue'
import LoginOrUser from './components/LoginOrUser.vue'
import TelegramLogin from './components/TelegramLogin.vue'
import { useAuth } from './stores/auth'

const mode = ref<'library' | 'search'>('library')
const auth = useAuth()
const isAuthed = computed(() => auth.isAuthenticated)

function updateBodyClass() {
  if (isAuthed.value) {
    document.body.classList.add('auth')
    document.body.classList.remove('unauth')
  } else {
    document.body.classList.add('unauth')
    document.body.classList.remove('auth')
  }
}

onMounted(updateBodyClass)
watch(isAuthed, updateBodyClass)
</script>


