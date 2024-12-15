<template>
  <div class="flex flex-col bg-white p-1 gap-1 h-fit">
    <img class="w-full max-w-[256px] max-h-[256px]" :src="src || game_images[game_alias].character"/>
    <div class="rotate-[6deg] md:hidden text-md font-nanum-brush text-center text-content-secondary">{{
        name
      }}
    </div>
  </div>
</template>

<script setup lang="ts">
import {game_images} from "@/constants/gameImages";

const props = defineProps(['game_alias', 'src', 'name'])
</script>
