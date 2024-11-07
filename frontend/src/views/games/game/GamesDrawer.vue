<template>
  <div class="flex flex-col gap-3 px-3'">
    <div class="flex flex-row items-center gap-3 text-4xl text-semibold uppercase text-content-secondary mb-6">
      <inline-svg class="w-12 h-12 rotate-180" :src="require('@/assets/images/icons/common/arrow.svg')"/>
      Сетка ролей
    </div>
    <div class="flex flex-col gap-3 pl-6" v-if="family_groups">
      <div class="text-2xl uppercase font-semibold text-content-secondary mb-3">По семьям</div>
      <GroupNamesBlock
          v-for="group in family_groups.filter(g => g.characters.length>0)" :key="group"
          :game_alias="game_alias" :group="group"
      />
    </div>
    <div class="flex flex-col gap-3 pl-6" v-if="group_groups">
      <div class="text-2xl font-semibold text-content-secondary mb-3"> По занятости</div>
      <GroupNamesBlock
          v-for="group in group_groups.filter(g => g.characters.length>0)"
          :key="group" :game_alias="game_alias" :group="group"
          @click="$router.push(`/game/${game_alias}/roles#${group.name}`)"
      />
    </div>
  </div>
</template>


<script setup lang="ts">
import {ref} from "vue"
import {useStore} from "vuex";
import GroupNamesBlock from "@/views/games/groups/GroupNamesBlock.vue";

const store = useStore()
const user = store.getters['auth/user']
const props = defineProps({
  'game_alias': {type: String},
  'group_groups': {type: Array},
  'family_groups': {type: Array},
})
const game = ref({
  id: 1,
  title: "lorem ipsum",
  image: null,
  groups: [],
  non_grouped: []
})

const others = {
  "frostpunk": {name: "Жители Нью-Ливерпуля", description: ""},
  "whales": {name: "Жители Тресё", description: ""},
}[props.game_alias]

const others_group = {
  image: null,
  name: others.name,
  description: others.description,
  characters: game.value.non_grouped, subgroups: []
}
</script>
