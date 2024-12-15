<template>
  <div class="flex flex-col w-full gap-1">
    <div class="text-xl">Telegram</div>
    <div class="flex flex-col md:flex-row md:items-center gap-1 md:gap-6">
      <div class="text-xl text-content-disabled">{{ user.telegram ? '@' + user.telegram : "Не подключен" }}</div>
      <div class="flex flex-row items-center gap-3">
        <button class="btn-gradient" @click="openTelegram"> {{ $t(`common.actions.openBot`) }}</button>
        <button v-if="!user.telegram" @click="copyLink" class="flex items-center justify-center gap-3 py-0">
          <inline-svg class="w-8 h-8" :src="require(`@/assets/images/icons/common/${copied ? 'check' : 'copy'}.svg`)"/>
          {{ copied ? $t(`common.linkCopied`) : $t(`common.actions.copy`) }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, ref} from "vue"
import {useStore} from "vuex"

const store = useStore()
const user = computed(() => store.getters["auth/user"])
const copied = ref(false)


const copyLink = () => {
  navigator.clipboard.writeText(user.value.telegram_code)
  copied.value = true
  setTimeout(() => copied.value = false, 3000)
}
const openTelegram = () => {
  const url = "https://t.me/tomatoboto_bot" + (user.value.telegram ? "" : `?start=${user.value.telegram_code}`)
  window.open(url, '_blank').focus()
}
</script>
