<template>
  <div class="flex flex-col p-6 gap-6 rounded-xl bg-gray-700 bg-opacity-60 mt-48 mx-3">
    <div class="flex max-md:flex-col max-md:justify-center items-center gap-6 relative">
      <Avatar
          class="min-w-[128px]" size="128" :src="user.avatar"
          :username="user.first_name + ' ' + user.last_name"
      ></Avatar>
      <div class="flex flex-col gap-1 max-md:items-center justify-center">
        <span class="text-2xl">
          {{ user.first_name }} {{ user.last_name }} | {{ user.username }}
        </span>
        <span class="text-content-disabled text-gray-400">{{ user.email }}</span>
      </div>
      <button
          @click="$router.push('/account/settings')"
          class="btn-gray gap-2 max-md:w-full md:absolute top-6 right-6">
        <inline-svg :src="require('@/assets/images/icons/account/settings.svg')"/>
        {{ $t("menu.settings") }}
      </button>
    </div>
    <ApplicationTable/>
  </div>
</template>

<script setup>
import {computed} from "vue"
import {useStore} from "vuex"
import {useI18n} from "vue-i18n"
import Avatar from "@/components/Avatar.vue";
import ApplicationTable from "@/views/account/ApplicationTable.vue";


const {t} = useI18n()
const store = useStore()
const user = computed(() => store.getters["auth/user"])
</script>
