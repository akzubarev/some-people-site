<template>
  <div class="flex flex-col gap-3">
    <div class="flex flex-row gap-6 w-full justify-between pl-10">
      <div class="text-lg text-content-primary whitespace-pre-wrap">
          <span class="text-2xl text-content-primary font-bold">{{
              subfaction.name
            }}{{ (subfaction.description) ? " — " : "" }}
          </span> {{ subfaction.description }}
      </div>
    </div>
    <div class="flex bg-repeat-y h-full z-10">
      <div class="flex flex-col pl-20 pr-6 gap-3">
        <CharacterBlock
            v-for="character in subfaction.characters" :key="character"
            :character="character" :game="game"/>
      </div>
    </div>
  </div>
</template>


<script setup>
import CharacterBlock from "@/views/games/factions/CharacterBlock.vue";

const props = defineProps({
  subfaction: {
    type: Object,
    default: {
      id: 1,
      name: "lorem ipsum",
      description: "lorem ipsum",
      game: 1,
      parent: null,
      image: null,
      characters: []
    }
  },
  game: {
    type: String,
  }
})
</script>
