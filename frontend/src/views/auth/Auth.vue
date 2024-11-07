<template>
  <div class="flex relative w-full h-full min-h-screen items-center justify-center align-center bg-bg-primary">
    <img class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 h-full opacity-40 z-0"
         :src="require('@/assets/images/logo/moth.svg')"/>
    <div class="flex flex-col w-full lg:w-1/2 p-6 gap-3 items-center rounded-2xl bg-bg-transparent-2 z-10">
      <div class="text-2xl text-center">Авторизация</div>
      <router-view/>
      <router-link
          class="text-lg text-active-primary underline me-6"
          :to=" $route.path.includes('sign-up') ? '/sign-in': '/sign-up'"
      >
        {{ $route.path.includes('sign-up') ? $t("auth.signIn") : $t("auth.signUp") }}
      </router-link>
    </div>
  </div>
</template>
<script setup lang="ts">
import {useI18n} from "vue-i18n";

const {t} = useI18n()

</script>
