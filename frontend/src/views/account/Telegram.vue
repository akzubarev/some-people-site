<template>
  <div class="card p-6 flex flex-col gap-3 mt-6">
      <h1
        v-if="user.telegram"
        class="font-normal">
        <div class="flex justify-start w-full items-center gap-5 mb-5">
          <div class="rounded-full w-[3rem] h-[3rem] bg-[#0F9959] flex justify-center items-center">
            <inline-svg class="text-black" width="25" height="25" :src="require(`@/assets/images/icons/common/check.svg`)" />
          </div>
          {{ user.telegram ? '@' + user.telegram : "" }}
        </div>
        <span class="text-2xl">{{ $t("settings.telegram.enabled") }}</span>
      </h1>
      <h1 v-else class="font-normal">
        {{ $t("settings.telegram.disabled") }}
      </h1>
      <div
        class="fs-5"
        v-if="!user.telegram"
        v-html="$t('settings.telegram.linkDisabled')"
      />
      <div
        v-else class="fs-5"
        v-html="$t('settings.telegram.linkEnabled')"
      />
      <div class="flex max-sm:flex-col w-full justify-start md:w-auto gap-4 mt-3">
        <button
        class="btn btn-accent flex-shrink-0"
          @click="openTelegram"
        >
          {{ $t(`common.actions.openChat`) }}
        </button>
        <button
          class="btn  py-0 flex-shrink-0 flex justify-center items-center gap-2"
          @click="copyLink">
          <inline-svg class="fs-3" :src="require(`@/assets/images/icons/common/${copied ? 'check' : 'Copy'}.svg`)" />
          {{ copied ? $t(`common.linkCopied`) : $t(`common.actions.copy`)}}
        </button>
      </div>
    </div>
</template>

<script setup>
  import { onMounted, ref } from "vue"
  import notificationService from "@/services/notificationService"
  import { toClipboard } from "@soerenmartius/vue3-clipboard"
  import {useStore} from "vuex"

  const store = useStore()
  const user = store.getters["auth/user"]
  const copied = ref(false)
  const telegram = ref({})

  onMounted(async () => {
    telegram.value = (await notificationService.telegram())["data"]
  })

  const bot = "pin2pay_bot"
  const copyLink = () => {
    /* @ts-ignore */
    toClipboard(telegram.value.code)
    copied.value = true
    setTimeout(() => copied.value = false, 3000)
  }
  const openTelegram = () => {
    window.open(`https://t.me/${bot}?start=${telegram.value.code}`, '_blank').focus()
  }
</script>
