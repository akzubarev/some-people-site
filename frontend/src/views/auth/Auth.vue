<template>
  <div class="flex relative w-full h-full min-h-screen items-center justify-center align-center bg-bg-primary">
    <inline-svg
        class="absolute top-[65%] left-1/2 transform -translate-x-1/2 -translate-y-1/2
        h-[180%] overflow-hidden text-content-primary opacity-20 z-0"
        :src="require('@/assets/images/logo/mg.svg')"
    />
    <div class="flex flex-col w-full lg:w-1/2 p-6 gap-3 items-center rounded-2xl bg-bg-transparent-2 z-10">
      <div class="text-2xl text-center">Авторизация</div>
      <router-view/>
      <router-link class="text-lg text-content-primary text-center" to="/"> Обратно на главную</router-link>
    </div>
  </div>
</template>
<script setup lang="ts">
import {useI18n} from "vue-i18n";

const {t} = useI18n()

</script>
