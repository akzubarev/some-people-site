<template>
  <div ref="popupContainer" class="relative">
    <div @click="toggle">
      <slot name="header"/>
    </div>
<!--    <div class="relative">-->
      <div v-if="showPopup" class="absolute top-[100%] right-0 bg-bg-transparent rounded-xl" @click.stop>
        <slot name="content"/>
      </div>
<!--    </div>-->
  </div>
</template>

<script setup lang="ts">
import {onMounted, onUnmounted, ref} from 'vue'

const showPopup = ref(false)
const popupContainer = ref(null)

const toggle = () => {
  showPopup.value = !showPopup.value
}

const handleClickOutside = (event) => {
  if (popupContainer.value && !popupContainer.value.contains(event.target)) {
    showPopup.value = false
  }
}

onMounted(() => {
  document.addEventListener("click", handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside)
})
</script>