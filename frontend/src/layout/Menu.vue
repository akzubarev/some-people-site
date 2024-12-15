<template>
  <div id="menu" class="flex" :class="horizontal ? 'flex-row justify-end w-full gap-[5%] lg:gap-[15%]' : 'flex-col gap-6'">
    <ActionModal
        v-if="showLocked" type="lock"
        @close="() => {showLocked = false}"
        @submit="() => {showLocked = false}"
        :title="lockedText" :buttonText="$t('common.actions.ok')">
    </ActionModal>
    <div v-for="link in links" :key="link"
         @click="link.locked ? lockedSection(link.lockedText) : () => {$emit('closeDrawer'); $router.push(link.link)}"
         class="text-header uppercase flex flex-row gap-1 items-center cursor-pointer"
         :class="link.locked ? 'text-content-disabled' : 'hover:text-content-accent'">
      {{ link.title }}
      <inline-svg
          v-if="link.locked" class="h-6 w-6 text-content-disabled"
          :src="require('@/assets/images/icons/common/lock.svg')"/>
    </div>
  </div>
</template>
<script setup lang="ts">

import {ref} from 'vue'
import ActionModal from "@/components/ActionModal.vue";

defineProps(['horizontal'])
defineEmits(['closeDrawer'])


const showLocked = ref(false)
const lockedText = ref("Раздел в разработке")

const lockedSection = (text) => {
  lockedText.value = text
  showLocked.value = true
}

const links = [
  // {
  //   title: "Игры",
  //   link: "/games",
  //   locked: true,
  //   lockedText: "Раздел в разработке",
  // },
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