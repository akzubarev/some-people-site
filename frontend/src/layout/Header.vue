<template>
  <ActionModal
      v-if="showLocked" type="lock"
      @close="() => {showLocked = false}"
      @submit="() => {showLocked = false}"
      :title="lockedText" :buttonText="$t('common.actions.ok')">
  </ActionModal>
  <img class="absolute ml-2 mt-2 h-22 w-22 z-10 opacity-75" :src="require('@/assets/images/logo/moth.svg')"/>
  <Avatar
      class="absolute right-3 top-8 h-24 w-24 z-30 cursor-pointer"
      :src="user.avatar" @click="$router.push('/account/profile')"
      :username="user ? `${user.first_name} ${user.last_name}` : 'Анонимный пользователь'"
  />
  <div class="absolute w-full bg-bg-transparent p-3 mt-10 pl-20 pr-60 z-20">
    <div class="flex flex-row w-full gap-3 justify-between h-14 py-3">
      <div class="text-3xl font-semibold text-uppercase cursor-pointer hover:text-content-accent" @click=" $router.push('/')">
        <inline-svg @click="$emit('asideToggle')" class="lg:hidden cursor-pointer"
                    :src="require('@/assets/images/icons/common/menu.svg')"/>
        {{ 'Какие-то люди'  }}
      </div>
      <div class="flex flex-row gap-32">
        <div v-for="link in links" :key="link"
             @click="link.locked ? lockedSection(link.lockedText) : $router.push(link.link)"
             class="text-3xl text-uppercase flex flex-row gap-1 items-center cursor-pointer"
             :class="link.locked ? 'text-content-disabled' : 'hover:text-content-accent'">
          {{ link.title }}
          <inline-svg
              v-if="link.locked" class="h-6 w-6 text-content-disabled"
              :src="require('@/assets/images/icons/common/lock.svg')"/>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import {computed, ref} from 'vue'
import Avatar from "@/components/Avatar.vue"
import store from '@/store'
import ActionModal from "@/components/ActionModal.vue";
// import Aside from "@/layout/aside/Aside.vue";

const emits = defineEmits(['asideToggle'])
const user = computed(() => store.getters["auth/user"])


const showLocked = ref(false)
const lockedText = ref("Раздел в разработке")

const lockedSection = (text) => {
  lockedText.value = text
  showLocked.value = true
}

const links = [
  {
    title: "Игры",
    link: "/games",
  },
  {
    title: "Новичкам",
    link: "/",
    locked: true,
    lockedText: "Раздел находится в разработке",
  },
  {
    title: "МГ",
    link: "/mg",
  },
]
</script>
