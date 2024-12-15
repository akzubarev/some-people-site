<template>
  <div class="flex flex-col gap-3 p-3">
    <a class="flex flex-row items-center gap-3 text-header text-content-secondary mb-6"
       :href="`/game/${game_alias}/about`" v-if="!phoneScreen">
      <inline-svg class="w-6 h-6 rotate-180" :src="require('@/assets/images/icons/common/arrow.svg')"/>
      Назад
    </a>
    <div class="text-large font-semibold uppercase text-content-secondary mb-6" v-if="!phoneScreen"> Сетка ролей</div>
    <div class="flex flex-col overflow-y-scroll no-scrollbar gap-medium">
      <div id="families" class="flex flex-col gap-3" v-if="family_groups">
        <div class="text-medium uppercase font-bold text-content-secondary mb-3 cursor-pointer"
             :class="showFamilyGroups ? 'underline':''" @click="$emit('showFamily', true)">
          По семьям
        </div>
        <GroupNamesBlock
            v-for="group in family_groups.filter(g => !groupIsEmpty(g))"
            :key="group" :game_alias="game_alias" :group="group" @close-drawer="$emit('closeDrawer')"
        />
      </div>
      <div id="groups" class="flex flex-col gap-3" v-if="group_groups">
        <div class="text-medium uppercase font-bold text-content-secondary mb-3 cursor-pointer"
             :class="!showFamilyGroups ? 'underline':''" @click="$emit('showFamily', false)">
          По занятости
        </div>
        <GroupNamesBlock
            v-for="group in group_groups.filter(g => !groupIsEmpty(g))"
            :key="group" :game_alias="game_alias" :group="group"
        />
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import {computed} from "vue"
import {useStore} from "vuex";
import GroupNamesBlock from "@/views/games/roles/groups/GroupNamesBlock.vue";

const store = useStore()
const user = store.getters['auth/user']
defineEmits(['showFamily', 'closeDrawer'])
const props = defineProps({
  'game_alias': {type: String},
  'group_groups': {type: Array},
  'family_groups': {type: Array},
  'showFamilyGroups': {type: Boolean, default: true},
})
const game = computed(() => store.getters['games/games'][props.game_alias])
const groupIsEmpty = (group) => group.characters.length + group.members.length + group.subgroups.length == 0
const phoneScreen = computed(() => window.screen.width < 768)
</script>
