<template>
  <div :class="$style.menu">
    <template v-for="(item, i) in MainMenuConfig()" :key="i">
      <div v-for="(pages, ji) in item.pages" :key="ji"
           :class="[ji&&'mt-10']">
        <template v-for="(menuItem, j) in pages" :key="j">
          <div :class="[j&&'mt-1']">
            <router-link
                v-slot="{ href,  navigate,  isActive, isExactActive }"
                :to="menuItem.route" @click="onClick">
              <a :class="[(isActive||isExactActive) && $style.active, $style.item]"
                 :href="href" @click="navigate">
                <span v-if="menuItem.svgIcon" class="w-6">
                  <inline-svg class="h-6 w-6" :src="menuItem.svgIcon"/>
                </span>
                <span>{{ menuItem.heading }} </span>
              </a>
            </router-link>
          </div>
        </template>
      </div>
    </template>
  </div>
</template>
<script setup>
import {useRoute} from "vue-router"
import MainMenuConfig from "@/core/config/MainMenuConfig"

const route = useRoute()

const emit = defineEmits(['route'])
const onClick = () => {
  emit('route')
}

</script>
<style lang="scss" module>
.item {
  @apply flex gap-3 w-full rounded-2xl py-3 items-center px-3;
}

.active {
  @apply bg-gray-900;
}

// .menu {
//   @apply px-3
// }
</style>