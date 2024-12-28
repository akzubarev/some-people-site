<template>
  <div class="flex flex-col gap-2">
    <div class="flex flex-row gap-2 items-center cursor-pointer">
      <div v-if="group.subgroups?.length > 0" class="text-content-secondary text-sm"
           @click="expanded=!expanded" :class="expanded ? 'rotate-90' : ''"
      >
        ▶
      </div>
      <div class="text-medium leading-4 font-semibold text-content-secondary"
           :class="group.subgroups.length > 0 ? '' : 'ml-3'"
           @click="reroute(`#${group.name}`)">
        {{ group.name }}
      </div>
    </div>
    <div class="flex flex-col gap-3 pl-4" v-if="expanded">
      <GroupNamesBlock
          v-for="subgroup in group.subgroups.filter(s => s.characters.length+s.members.length+s.subgroups.length>0)"
          :key="subgroup" :group="subgroup" :game_alias="game_alias"
      />
    </div>
  </div>
</template>


<script setup lang="ts">
import {ref} from "vue";
import {useRouter} from "vue-router";

const router = useRouter()
const emit = defineEmits(["closeDrawer"])
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
      characters: []
    }
  },
  game_alias: {type: String},
  expanded: {type: Boolean, default: false},
})

const expanded = ref(props.expanded)
const reroute = (group_name) => {
  emit('closeDrawer')
  router.push(group_name)
}
</script>
