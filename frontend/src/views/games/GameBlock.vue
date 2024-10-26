<template>
  <ImageBanner
      :full="full" :image="{
        frostpunk:require('@/assets/images/games/frostpunk/background.png'),
        whales:require('@/assets/images/games/whales/background.jpg')
      }[game.alias]"
      :title="game.title"
      :description="full ? game.description : game.short_description"
      :tags="gameData"
      :buttons="[{text: 'Подробнее', href:`/game/${game.alias}/about`}]"
      :social="social"
  />
</template>


<script setup>
import ImageBanner from "@/components/ImageBanner.vue";

const props = defineProps({
  game: {
    type: Object,
    default: {
      id: 1,
      title: "lorem ipsum",
      _description: "lorem ipsum",
      short_description: "lorem ipsum",
      factions: []
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
