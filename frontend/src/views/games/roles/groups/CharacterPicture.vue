<template>
  <div class="flex flex-col bg-white p-1 gap-1 h-fit">
    <img class="w-full max-w-[256px] max-h-[256px]" :src="picture" :alt="name || 'Персонаж'" @error="imageFailed = true"/>
    <div class="rotate-[6deg] md:hidden text-md font-nanum-brush text-center text-content-secondary">{{
        name
      }}
    </div>
  </div>
</template>

<script setup lang="ts">
import {game_images} from "@/constants/gameImages";
import {computed, ref, watch} from 'vue';

const props = defineProps(['game_alias', 'src', 'name'])
const imageFailed = ref(false)
const picture = computed(() => (!imageFailed.value && props.src) || game_images[props.game_alias]?.character || require('@/assets/images/default_avatar.png'))
watch(() => [props.src, props.game_alias], () => { imageFailed.value = false })
</script>
