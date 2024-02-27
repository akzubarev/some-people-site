<template>
  <div class="flex flex-col gap-3">
    <div class="flex flex-row gap-6 w-full justify-between"
         @click="expanded=!expanded">
      <div class="text-lg text-white whitespace-pre-wrap">
          <span class="text-4xl text-white font-bold w-[95%]">{{
              faction.name
            }}{{ (expanded && faction.description) ? " — " : "" }}
          </span> {{ expanded ? faction.description : "" }}
      </div>
      <inline-svg
          class="!w-[20px]"
          :class="[s.arrow, { [s.arrow_expanded]: expanded }]"
          :src="require('@/assets/images/icons/common/chevrone.svg')"
      />
    </div>
    <div class="flex flex-row gap-1 w-full" v-if="expanded">
      <hr class="h-1 w-1 bg-gray-200 border-0 rounded">
      <hr class="h-1 w-full bg-gray-200 border-0 rounded">
      <hr class="h-1 w-1 bg-gray-200 border-0 rounded">
    </div>
    <div class="flex bg-repeat-y h-full z-10" v-if="expanded"
         :style="`background-image: url(${factions[game][faction.alias]})`">
      <div class="flex flex-col gap-3" v-if="expanded">
        <SubFactionBlock
            v-for="subfaction in faction.subfactions" :key="subfaction"
            :subfaction="subfaction" :game="game"
        />
      </div>
      <div class="flex flex-col pl-20 pr-6 gap-3">
        <CharacterBlock
            v-for="character in faction.characters" :key="character"
            :character="character" :game="game"/>
      </div>
    </div>
  </div>
</template>


<script setup>
import SubFactionBlock from "@/views/games/factions/SubFactionBlock.vue";
import CharacterBlock from "@/views/games/factions/CharacterBlock.vue";
import {ref} from "vue";
import s from "@/components/filters/styles.module.scss";
import {factions} from "@/views/games/factionImages";

const expanded = ref(false)
const props = defineProps({
  faction: {
    type: Object,
    default: {
      id: 1,
      name: "lorem ipsum",
      description: "lorem ipsum",
      game: 1,
      parent: null,
      image: null,
      subfactions: [],
      characters: []
    }
  },
  game: {
    type: String,
  }
})
</script>
