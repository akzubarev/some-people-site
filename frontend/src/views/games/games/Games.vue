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
import gamesService from "@/services/gamesService";

const games = ref([])
gamesService.games({}).then(({data}) => {
  games.value = data
})
</script>
