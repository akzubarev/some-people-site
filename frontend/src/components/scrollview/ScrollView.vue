<template>
  <div
      class="card relative w-full flex gap-6 snap-x snap-proximity overflow-x-auto p-6">
    <div v-for="(item, i) in scrollConfig" :key="item"
         :class="['snap-center card hover:bg-[#171A1F]',
         $style.scroll_item, item.active ? '' : 'disabled',
         selected===i ? 'bg-[#171A1F]' : '']"
         @click="selected=i; $emit('selected', selected)"
    >
      <div class="flex min-h-[174px] items-center">
        <img class="min-w-[174px]" :src="item.photo">
      </div>
      <span class="inline-block text-normal text-center lg:text-xl whitespace-pre-wrap max-w-[300px]">
        {{ item.title }}
      </span>
      <inline-svg
          height="25" width="25" v-if="!item.active" class="text-gray-400"
          :src="require('@/assets/images/icons/matrix/Lock.svg')"
      ></inline-svg>
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";

const props = defineProps(["scrollConfig", "type"])
defineEmits(["selected"])
const selected = ref(null)
</script>

<style lang="scss" module>
.scroll_item {
  @apply relative flex flex-col w-fit gap-3 p-4 cursor-pointer items-center;
  &.disabled {
    @apply cursor-default;
    & img {
    }
  }
}
</style>
