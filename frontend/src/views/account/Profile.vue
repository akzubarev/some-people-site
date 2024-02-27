<template>
  <div class="flex flex-col p-3 gap-3">
    <div
        class="rounded-xl bg-gray-700 bg-opacity-60 p-6 mt-48 flex
      max-md:flex-col max-md:justify-center items-center gap-6 relative">
      <Avatar
          class="min-w-[128px]" size="128" :src="user.avatar"
          :username="user.first_name + ' ' + user.last_name"
      ></Avatar>
      <div class="flex flex-col gap-1 max-md:items-center justify-center">
        <span class="text-2xl">{{ user.first_name }} {{
            user.last_name
          }}</span>
        <span class="text-normal text-gray-400">{{ user.email }}</span>
      </div>
      <!--    <button-->
      <!--        @click="$router.push('/account/settings')"-->
      <!--        class="btn bg-gray-800 text-white max-md:w-full flex gap-2 justify-center md:absolute top-6 right-6">-->
      <!--      <inline-svg :src="require('@/assets/images/icons/common/Settings.svg')"/>-->
      <!--      {{ $t("menu.settings") }}-->
      <!--    </button>-->
    </div>
    <Settings/>
  </div>
</template>

<script setup>
import {computed, onMounted, ref} from "vue"
import {useStore} from "vuex"
import {useI18n} from "vue-i18n"
import Avatar from "@/components/avatar";
import {Tooltip} from "bootstrap";
import Settings from "@/views/account/Settings.vue";


const {t} = useI18n()
const store = useStore()
const user = computed(() => store.getters["auth/user"])

onMounted(() => {
  const tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
  )
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new Tooltip(tooltipTriggerEl)
  })
})
</script>
