<template>
  <div class="card">
    <div class="card-header border-0">
      <div class="card-title">
        Игры
      </div>
    </div>
  </div>

  <div class="flex flex-col gap-6 mt-6">
    <GameBlock
        class="h-[500px]" :class="i % 2 === 1 ? 'justify-end': 'justify-start'"
        v-for="(game, i) in games" :key="game" :game="game"
        :full="false"/>
  </div>
</template>

<script setup>
import {ref} from "vue"
import GameBlock from "@/views/games/GameBlock.vue";
import gamesService from "@/services/gamesService";
import ImageBanner from "@/views/dashboard/ImageBanner.vue";

const games = ref([])
gamesService.games({}).then(({data}) => {
  games.value = data
})
</script>
