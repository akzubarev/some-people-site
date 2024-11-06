<template>
  <div class="flex flex-col bg-white px-2 pt-2 pb-3 gap-1">
    <img :src="src || characters[game_alias]['default']"/>
    <div class="text-lg font-semibold text-center text-content-secondary">{{ name }}</div>
  </div>
</template>

<script setup lang="ts">
import {characters} from "@/constants/characterImages";

const props = defineProps(['game_alias', 'src', 'name'])
</script>
