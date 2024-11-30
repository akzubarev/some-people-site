<template>
  <div class="flex flex-col gap-6 mt-48">
    <GameBlock
        class="rounded-xl h-[500px]" :class="i % 2 === 1 ? 'justify-end': 'justify-start'"
        v-for="(game, i) in games" :key="game" :game="game"
        :full="false"/>
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue"
import GameBlock from "@/views/games/games/GameBlock.vue";
import {useStore} from "vuex";

const store = useStore()
const games = ref(store['games/games'])
</script>
