<template>
  <div class="flex flex-col p-header gap-6 rounded-xl h-screen overflow-auto no-scrollbar">
    <div class="flex flex-col p-6 gap-6 rounded-xl bg-gray-700 bg-opacity-60 mx-3 mt-6">
      <div class="flex flex-row items-center gap-3 text-header text-content-primary"
           @click="$router.push(`/account/whales/application`)">
        <inline-svg class="w-6 h-6 rotate-180" :src="require('@/assets/images/icons/common/arrow.svg')"/>
        Назад
      </div>
      <ProfileSettings/>

      <Telegram/>
      <div class="form flex flex-col gap-3">
        <button @click="$router.push('/sign-out')"
                class="btn-primary ml-auto w-fit max-sm:w-full">
          {{ $t("menu.logout") }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import ProfileSettings from "@/views/account/settings/ProfileSettings.vue";
import Telegram from "@/views/account/settings/Telegram.vue";
</script>
