<template>
  <div v-if="open" class="fixed inset-0 z-50 grid place-items-center bg-black/50" @click.self="close">
    <div class="w-[min(92vw,680px)] rounded-xl bg-base-800 p-5 shadow-innerdeep">
      <div class="mb-4 text-accent-300 text-lg">Tags</div>
      <div class="flex gap-2 mb-4">
        <input v-model="query" @keyup.enter="resetAndSearch" placeholder="Search tags" class="flex-1 bg-base-700 rounded px-4 py-3 outline-none focus:ring-1 focus:ring-accent-400 text-base" />
        <button @click="resetAndSearch" class="px-4 py-3 rounded bg-base-600 hover:bg-base-500 text-base">Search</button>
      </div>
      <div ref="scrollBox" class="min-h-28 max-h-80 overflow-auto pr-1 space-y-1">
        <div v-if="!loading && results.length===0" class="text-accent-400 text-sm">
          No tags. <button @click="createTag" class="underline">Create tag</button>
        </div>
        <div v-for="t in results" :key="t" class="flex items-center justify-between bg-base-700 rounded px-3 py-2">
          <div class="text-accent-300 text-base">#{{ t }}</div>
          <input type="checkbox" class="scale-110" :checked="selectedSet.has(t)" @change="toggle(t)" />
        </div>
      </div>
      <div class="mt-5 flex justify-end gap-3">
        <button @click="apply" class="px-4 py-2 rounded bg-base-600 hover:bg-base-500 text-base">Add</button>
        <button @click="close" class="px-4 py-2 rounded bg-base-600 hover:bg-base-500 text-base">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps<{ open: boolean; initialSelected: string[] }>()
const emit = defineEmits(['close','apply'])

const query = ref('')
const loading = ref(false)
const results = ref<string[]>([])
const selectedSet = ref<Set<string>>(new Set(props.initialSelected || []))
const nextUrl = ref<string | null>(null)
const scrollBox = ref<HTMLElement | null>(null)

watch(() => props.initialSelected, (v) => { selectedSet.value = new Set(v || []) })
watch(() => props.open, (o) => { if (o) resetAndSearch() })

function normalize(u: string) { try { const a = new URL(u); return a.pathname + a.search } catch { return u } }

async function search(append = false) {
  loading.value = true
  try {
    const base = '/api/tags/'
    const url = append && nextUrl.value ? normalize(nextUrl.value) : `${base}?search=${encodeURIComponent(query.value)}`
    const resp = await axios.get(url)
    const page = (resp.data?.results || []).map((x: any) => x.name)
    results.value = append ? results.value.concat(page) : page
    nextUrl.value = resp.data?.next || null
  } finally { loading.value = false }
}

function resetAndSearch() { nextUrl.value = null; results.value = []; search(false) }

function toggle(t: string) {
  const s = selectedSet.value
  if (s.has(t)) s.delete(t); else s.add(t)
}

function createTag() {
  const name = query.value.trim()
  if (!name) return
  if (!results.value.includes(name)) results.value.unshift(name)
  selectedSet.value.add(name)
  query.value = ''
}

function apply() {
  emit('apply', Array.from(selectedSet.value))
  close()
}

function close() { emit('close') }

onMounted(() => {
  const el = scrollBox.value
  if (!el) return
  el.addEventListener('scroll', () => {
    if (!nextUrl.value || loading.value) return
    if (el.scrollTop + el.clientHeight >= el.scrollHeight - 20) {
      search(true)
    }
  })
})
</script>


