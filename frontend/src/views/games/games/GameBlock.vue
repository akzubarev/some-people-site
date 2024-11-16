<template>
  <ImageBanner
      :title="game.title" :image="game_images[game.alias]['background']"
      :description="full ? game.description : game.short_description"
      :buttons="[{text: 'Подробнее', href:`/game/${game.alias}/about`}]"
      :tags="gameData" :social="social" :full="full"
  />
</template>


<script setup lang="ts">
import ImageBanner from "@/components/ImageBanner.vue";
import {game_images} from "@/constants/gameImages";

const props = defineProps({
  game: {
    type: Object,
    default: {
      id: 1,
      title: "lorem ipsum",
      _description: "lorem ipsum",
      short_description: "lorem ipsum",
      groups: []
    }
  },
  full: {
    type: Boolean,
    default: false
  }
})


const formatDate = date => {
  return new Date(date).toLocaleDateString(
      'ru', {
        day: "numeric",
        month: "numeric",
        // year: "numeric",
        hour: "numeric",
        minute: "numeric"
      })
}
const gameData = [
  props.game.year,
  `${formatDate(props.game.start)} - ${formatDate(props.game.end)}`,
  props.game.location
]

const social = {
  "vk": props.game.vk,
  "tg": props.game.tg,
  // "ig": props.game.vk,
}
</script>
