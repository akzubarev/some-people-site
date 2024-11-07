<template>
  <div class="flex flex-col gap-3">
    <div class="flex flex-col gap-1" :id="group.name">
      <div class="flex flex-col pl-[17%] w-[80%] gap-3">
        <div class="text-4xl text-content-secondary font-semibold uppercase">{{ group.name }}</div>
        <div class="text-lg text-content-secondary font-semibold">{{ group.description }}</div>
      </div>
      <div class="flex flex-col gap-3">
        <CharacterBlock
            v-for="character in group.characters" :key="character"
            :character="character" :game_alias="game_alias"
        />
      </div>
      <div class="flex flex-col gap-3">
        <GroupBlock
            v-for="subgroup in group.subgroups" :key="subgroup"
            :subgroup="subgroup" :game_alias="game_alias"
        />
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import CharacterBlock from "@/views/games/groups/CharacterBlock.vue";

const props = defineProps({
  group: {
    type: Object,
    default: {
      id: 1,
      name: "lorem ipsum",
      description: "lorem ipsum",
      game: 1,
      parent: null,
      image: null,
      subgroups: [],
      characters: []
    }
  },
  game_alias: {type: String},
})
</script>
