<template>
  <div class="flex flex-col gap-3">
    <div class="flex flex-row gap-1 items-center cursor-pointer">
      <inline-svg
          v-if="group.subgroups?.filter(g => g.characters.length > 0).length > 0"
          class="text-content-secondary" @click="expanded=!expanded"
          :src="require('@/assets/images/icons/common/chevrone.svg')"
      />
      <div class="text-xl text-content-secondary" :class="expanded ? 'rotate-180' : ''"
           @click="$router.push(`#${group.name}`)">
        {{ group.name }}
      </div>
    </div>
    <div class="flex flex-col gap-3 pl-1" v-if="expanded">
      <GroupNamesBlock
          v-for="subgroup in group.subgroups" :key="subgroup"
          :subgroup="subgroup" :game_alias="game_alias"
      />
    </div>
  </div>
</template>


<script setup>
import {ref} from "vue";

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
  game_alias: {type: String},
})
</script>
