<template>
  <div class="flex flex-col gap-3">
    <div class="flex flex-row gap-6 w-full justify-between pl-10">
      <div class="text-lg whitespace-pre-wrap">
          <span class="text-2xl font-bold">{{
              subgroup.name
            }}{{ (subgroup.description) ? " — " : "" }}
          </span> {{ subgroup.description }}
      </div>
    </div>
    <div class="flex bg-repeat-y h-full z-10">
      <div class="flex flex-col pl-20 pr-6 gap-3">
        <CharacterBlock v-for="character in subgroup.characters" :key="character"
                        :character="character" :game="game"/>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import CharacterBlock from "@/views/games/roles/groups/CharacterBlock.vue";

const props = defineProps({
  subgroup: {
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
  game: {type: String},
})
</script>
