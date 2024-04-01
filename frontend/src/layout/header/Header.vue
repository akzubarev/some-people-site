<template>
  <ActionModal
      v-if="showLocked" type="lock"
      @close="() => {showLocked = false}"
      @submit="() => {showLocked = false}"
      :title="lockedText" :buttonText="$t('common.actions.ok')">
  </ActionModal>
  <div class="w-full bg-gray-800 bg-opacity-70 absolute p-3 mt-10 z-20">
    <div class="flex flex-row w-full gap-3 justify-between h-14 py-3">
      <inline-svg @click="$emit('asideToggle')"
                  class="lg:hidden cursor-pointer"
                  :src="require('@/assets/images/icons/common/menu.svg')"/>
      <div
          class="flex flex-row gap-5 justify-between pl-20 w-3/4">
        <div v-for="link in links" :key="link"
             @click="link.locked ? lockedSection(link.lockedText) : $router.push(link.link)"
             class="text-3xl font-bold flex flex-row gap-1 items-center cursor-pointer"
             :class="link.locked ? 'text-gray-500' : 'hover:text-gray-300'">
          {{ link.title }}
          <inline-svg
              v-if="link.locked" class="h-[25px] w-[25px] text-gray-500"
              :src="require('@/assets/images/icons/matrix/Lock.svg')"/>
        </div>
      </div>
      <div class="flex items-center cursor-pointer w-1/4 justify-end">
        <Avatar
            :src="user.avatar" :rounded="true"
            size="50" @click="$router.push('/account/profile')"
            :username="user ? `${user.first_name} ${user.last_name}` : 'Анонимный пользователь'"
        />
      </div>
    </div>
  </div>
</template>


<script setup>
import {computed, ref} from 'vue'
import Avatar from "@/components/avatar"
import store from '@/store'
import ActionModal from "@/components/action-modal/ActionModal.vue";
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
    locked: true,
    lockedText: "Раздел находится в разработке",
  },
  {
    title: "МГ",
    link: "/mg",
  },
]
</script>
