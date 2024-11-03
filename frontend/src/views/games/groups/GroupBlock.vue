<template>
  <div class="flex flex-col gap-3">
    <div class="flex flex-row gap-6 w-full justify-between" @click="expanded=!expanded">
      <div class="text-lg whitespace-pre-wrap">
          <span class="text-4xl font-bold w-[95%]">{{
              group.name
            }}{{ (expanded && group.description) ? " — " : "" }}
          </span> {{ expanded ? group.description : "" }}
      </div>
      <inline-svg
          class="!w-[20px]" :class="[s.arrow, { [s.arrow_expanded]: expanded }]"
          :src="require('@/assets/images/icons/common/chevrone.svg')"
      />
    </div>
    <div class="flex flex-row gap-1 w-full" v-if="expanded">
      <hr class="h-1 w-1 bg-gray-200 border-0 rounded">
      <hr class="h-1 w-full bg-gray-200 border-0 rounded">
      <hr class="h-1 w-1 bg-gray-200 border-0 rounded">
    </div>
    <div class="flex bg-repeat-y h-full z-10" v-if="expanded"
         :style="`background-image: url(${groups[game][group.alias]})`">
      <div class="flex flex-col gap-3" v-if="expanded">
        <SubGroupBlock v-for="subgroup in group.subgroups" :key="subgroup"
                         :subgroup="subgroup" :game="game"/>
      </div>
      <div class="flex flex-col pl-20 pr-6 gap-3">
        <CharacterBlock v-for="character in group.characters" :key="character"
                        :character="character" :game="game"/>
      </div>
    </div>
  </div>
</template>


<script setup>
import SubGroupBlock from "@/views/games/groups/SubGroupBlock.vue";
import CharacterBlock from "@/views/games/groups/CharacterBlock.vue";
import {ref} from "vue";
import s from "@/components/styles.module.scss";
import {groups} from "@/constants/groupImages";

const expanded = ref(false)
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
  game: {type: String},
})
</script>
