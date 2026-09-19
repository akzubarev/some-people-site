<template>
  <div class="flex flex-col w-full gap-3">
    <div class="text-xl">Telegram</div>
    <div>{{ user.telegram ? '@' + user.telegram : 'Не подключен' }}</div>
    <button class="btn-primary" :disabled="pending" @click="createLink">
      {{ pending ? 'Получение ссылки…' : user.telegram ? 'Переподключить Telegram' : 'Подключить Telegram' }}
    </button>
    <p v-if="error" role="alert">{{ error }}</p>
    <div v-if="link" class="flex flex-col gap-2">
      <p>Ссылка действует 10 минут и используется один раз. Не передавайте её другим людям.</p>
      <a class="btn-primary" :href="link.url" target="_blank" rel="noopener noreferrer">Открыть бота</a>
      <button @click="copyCode">{{ copied ? 'Код скопирован' : 'Скопировать код' }}</button>
    </div>
  </div>
</template>
<script setup lang="ts">
import {computed, ref, onBeforeUnmount} from 'vue'
import {useStore} from 'vuex'
import authService from '@/services/authService'

const store = useStore()
const user = computed(() => store.getters['auth/user'])
const link = ref(null)
const copied = ref(false)
const pending = ref(false)
const error = ref('')
let expiryTimer: ReturnType<typeof setTimeout>
const createLink = async () => {
  pending.value = true
  error.value = ''
  link.value = null
  copied.value = false
  clearTimeout(expiryTimer)
  try {
    const {data} = await authService.telegramLink()
    link.value = data
    expiryTimer = setTimeout(() => { link.value = null }, data.expires_in * 1000)
  } catch {
    error.value = 'Не удалось получить ссылку. Повторите попытку.'
  } finally {
    pending.value = false
  }
}
const copyCode = async () => {
  try {
    await navigator.clipboard.writeText(link.value.code)
    copied.value = true
  } catch {
    error.value = 'Не удалось скопировать код. Используйте кнопку «Открыть бота».'
  }
}
onBeforeUnmount(() => clearTimeout(expiryTimer))
</script>
