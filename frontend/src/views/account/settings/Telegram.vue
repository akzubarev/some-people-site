<template>
  <div class="flex flex-wrap">
    <label class="flex items-center basis-full lg:basis-1/3 text-content-primary"> Telegram </label>
    <div class="flex flex-row items-center justify-between px-3 gap-3 basis-full lg:basis-2/3 mt-2 lg:mt-0">
      <span class="text-xl text-content-disabled">{{ user.telegram ? '@' + user.telegram : "Не подключен" }}</span>
      <div class="flex flex-row items-center gap-3
">
        <button class="btn-gradient flex-shrink-0" @click="openTelegram">
          {{ $t(`common.actions.openBot`) }}
        </button>
        <button v-if="!user.telegram" @click="copyLink"
                class="btn py-0 flex-shrink-0 flex justify-center items-center gap-2">
          <inline-svg class="fs-3" :src="require(`@/assets/images/icons/common/${copied ? 'check' : 'copy'}.svg`)"/>
          {{ copied ? $t(`common.linkCopied`) : $t(`common.actions.copy`) }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed, ref} from "vue"
import {toClipboard} from "@soerenmartius/vue3-clipboard"
import {useStore} from "vuex"

const store = useStore()
const user = computed(() => store.getters["auth/user"])
const copied = ref(false)


const copyLink = () => {
  /* @ts-ignore */
  toClipboard(user.value.telegram_code)
  copied.value = true
  setTimeout(() => copied.value = false, 3000)
}
const openTelegram = () => {
  const url = "https://t.me/tomatoboto_bot" + user.value.telegram ? '' : `start=${user.value.telegram_code}`
  window.open(url, '_blank').focus()
}
</script>
