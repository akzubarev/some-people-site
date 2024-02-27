<template>
  <div class="w-full bg-gray-800 bg-opacity-70">
    <div class="flex flex-row w-full gap-3 justify-between h-14 py-3">
      <inline-svg @click="$emit('asideToggle')"
                  class="lg:hidden cursor-pointer"
                  :src="require('@/assets/images/icons/common/menu.svg')"/>
      <div
          class="flex flex-row gap-5 justify-between pl-20 w-3/4">
        <div v-for="link in links" :key="link"
             @click="$router.push(link.link)"
             class="text-3xl font-bold cursor-pointer">
          {{ link.title }}
        </div>
      </div>
      <div class="flex items-center cursor-pointer w-1/4 justify-end">
        <Avatar
            :src="user.avatar" :rounded="true"
            size="50" @click="$router.push('/account/profile')"
            :username="user.first_name + ' ' + user.last_name"
        />
      </div>
    </div>
  </div>
</template>


<script setup>
import {computed} from 'vue'
import Avatar from "@/components/avatar"
import store from '@/store'
// import Aside from "@/layout/aside/Aside.vue";

const emits = defineEmits(['asideToggle'])
const user = computed(() => store.getters["auth/user"])
const links = [
  {
    title: "Какие-то люди",
    link: "/",
  },
  {
    title: "Игры",
    link: "/games",
  },
  {
    title: "Новичкам",
    link: "/",
  },
  {
    title: "МГ",
    link: "/",
  },
]
</script>
