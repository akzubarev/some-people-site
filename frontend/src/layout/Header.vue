<template>
  <ActionModal
      v-if="showLocked" type="lock"
      @close="() => {showLocked = false}"
      @submit="() => {showLocked = false}"
      :title="lockedText" :buttonText="$t('common.actions.ok')">
  </ActionModal>
  <div class="absolute w-full bg-bg-transparent p-1 mt-6 z-50">
    <div class="flex flex-row w-full gap-small justify-between items-center h-12 pl-10 pr-3">
      <div id="title" @click=" $router.push('/')"
           class="flex flex-row w-full text-content-accent hover:text-content-primary items-center text-header font-semibold text-uppercase cursor-pointer"
      >
        <inline-svg
            class="h-16 w-16 md:hidden cursor-pointer" @click="$emit('asideToggle')"
            :src="require('@/assets/images/icons/common/menu.svg')"
        />
        Какие-то
        <inline-svg class="h-24 w-16 ml-2 py-1 -mt-2 -mb-3"
                    :src="require('@/assets/images/logo/mg.svg')"/>
        юди
      </div>
      <div id="menu" class="sm:hidden md:flex flex-row gap-16 lg:gap-24">
        <div v-for="link in links" :key="link"
             @click="link.locked ? lockedSection(link.lockedText) : $router.push(link.link)"
             class="text-large text-uppercase flex flex-row gap-xs items-center cursor-pointer"
             :class="link.locked ? 'text-content-disabled' : 'hover:text-content-accent'">
          {{ link.title }}
          <inline-svg
              v-if="link.locked" class="h-6 w-6 text-content-disabled"
              :src="require('@/assets/images/icons/common/lock.svg')"/>
        </div>
      </div>
      <Avatar
          class="h-20 w-20 ml-12 cursor-pointer"
          :src="user.avatar" @click="$router.push('/account/whales/application')"
      />
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
    locked: true,
    lockedText: "Раздел в разработке",
  },
  {
    title: "Новичкам",
    link: "/novices",
    locked: true,
    lockedText: "Раздел в разработке",
  },
  {
    title: "МГ",
    link: "/mg",
    locked: true,
    lockedText: "Раздел в разработке",
  },
]
</script>
