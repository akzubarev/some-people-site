<template>
  <div class="flex flex-col gap-3 p-3 pr-6">
    <a class="flex flex-row items-center gap-3 text-header text-content-secondary mb-6"
       :href="`/game/${game_alias}/about`" v-if="!phoneScreen">
      <inline-svg class="w-6 h-6 rotate-180" :src="require('@/assets/images/icons/common/arrow.svg')"/>
      Назад
    </a>
    <div class="text-large font-semibold uppercase text-content-secondary mb-6" v-if="!phoneScreen"> Сетка ролей</div>
    <div class="flex flex-col overflow-y-auto no-scrollbar gap-medium">
      <div id="groups" class="flex flex-col gap-3">
        <div class="flex flex-col xl:flex-row mb-3 gap-1">
          <div class="flex flex-row uppercase font-bold text-content-secondary gap-1">
            По
            <div class="text-content-secondary cursor-pointer" :class="showFamilyGroups ? '':'underline'"
                 @click="$emit('showFamily', false)">
              занятости
            </div>
            /
          </div>
          <div class="text-content-secondary uppercase font-bold cursor-pointer" :class="showFamilyGroups ? 'underline':''"
               @click="$emit('showFamily', true)"> семьям
          </div>
        </div>
        <div class="flex flex-col gap-3">
          <GroupNamesBlock
              v-for="(group, i) in (showFamilyGroups ? family_groups : group_groups).filter(g => !groupIsEmpty(g))"
              :key="group" :game_alias="game_alias" :group="group" :expanded="i==0"
          />
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import {computed, ref} from "vue"
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
const phoneScreen = ref(window.innerWidth < 768)
const updateWidth = () => phoneScreen.value = window.innerWidth < 768
const onLeave = () => {
  window.removeEventListener('resize', updateWidth);
  window.removeEventListener('beforeunload', onLeave);
}
window.addEventListener('resize', updateWidth)
window.addEventListener('beforeunload', onLeave)
</script>
