<template>
  <div class="w-lg-500px rounded shadow-sm p-10 p-lg-15 mx-auto">
    <p v-if="error" role="alert">{{ error }}</p>
    <p v-else>Выход из системы…</p>
    <button v-if="error" class="btn-primary" :disabled="pending" @click="signOut">Повторить выход</button>
  </div>
</template>
<script setup lang="ts">
import {ref, onMounted} from 'vue'
import {useStore} from 'vuex'
import {useRouter} from 'vue-router'
import authService from '@/services/authService'

const store = useStore()
const router = useRouter()
// Keep the credential only here so a failed server revocation can be retried.
const token = store.getters['auth/token']
const pending = ref(false)
const error = ref('')
const signOut = async () => {
  pending.value = true
  error.value = ''
  await store.dispatch('auth/logout')
  try {
    if (token) await authService.logout(token)
    await router.replace({name: 'sign-in'})
  } catch (failure) {
    if (failure.response?.status === 401) await router.replace({name: 'sign-in'})
    else error.value = 'Данные на этом устройстве очищены, но завершить сеанс на сервере не удалось. Повторите попытку.'
  } finally {
    pending.value = false
  }
}
onMounted(signOut)
</script>
