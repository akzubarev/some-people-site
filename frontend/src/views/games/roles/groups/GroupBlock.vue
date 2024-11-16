<template>
  <div class="flex flex-col gap-3">
    <div class="flex flex-col gap-medium" :id="group.name">
      <div v-if="group.characters" class="flex flex-row w-[75%] gap-3">
        <img class="w-12 h-12" :src="group.image"/>
        <div class="flex flex-col">
          <div class="text-medium text-content-secondary font-bold uppercase"> {{ group.name }}</div>
          <div class="text-small text-content-secondary font-semibold">{{ group.description }}</div>
        </div>
      </div>
      <div v-if="group.characters" class="flex flex-col gap-3">
        <CharacterBlock
            v-for="character in group.characters" :key="character"
            :character="character" :game_alias="game_alias"
        />
      </div>
      <div class="flex flex-col gap-3">
        <GroupBlock
            v-for="subgroup in group.subgroups.filter(s=>s.characters.length+s.members.length+s.subgroups.length>0)"
            :key="subgroup" :group="subgroup" :game_alias="game_alias"
        />
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import CharacterBlock from "@/views/games/roles/groups/CharacterBlock.vue";

const props = defineProps({
  group: {
    default: {
      id: 1,
      name: "lorem ipsum",
      description: "lorem ipsum",
      game: 1,
      parent: null,
      image: null,
      subgroups: [],
      characters: [],
      members: [],
    }
  },
  game_alias: {type: String},
})

props.group.characters = props.group.characters.concat(props.group.members)
</script>
