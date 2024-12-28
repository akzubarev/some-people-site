<template>
  <div v-if="characters.length + displaySubgroups.length" class="flex flex-col gap-large" :id="group.name">
    <div v-if="characters.length" class="flex flex-col gap-small">
      <div class="flex items-center flex-row px-[2.5%] md:px-0 md:w-[80%] gap-3">
        <img v-if="!phoneScreen" class="w-12 h-12" :src="game_images[game_alias].group"/>
        <inline-svg v-else class="w-12 h-12 rotate-180 text-content-secondary"
                    @click="$emit('showDrawer')" :src="require('@/assets/images/icons/common/arrow.svg')"/>
        <div class="flex flex-col">
          <div class="text-medium text-content-secondary font-bold uppercase"> {{ group.name }}</div>
          <div class="text-small text-content-secondary font-semibold">{{ group.description }}</div>
        </div>
      </div>
      <div v-if="characters.length" class="flex flex-col gap-3">
        <CharacterBlock
            v-for="character in characters" :key="character"
            :character="character" :game_alias="game_alias"
        />
      </div>
    </div>
    <div v-if="displaySubgroups.length" class="flex flex-col gap-large">
      <GroupBlock
          v-for="subgroup in displaySubgroups" :key="subgroup"
          :group="subgroup" :game_alias="game_alias"
      />
    </div>
  </div>
</template>


<script setup lang="ts">
import CharacterBlock from "@/views/games/roles/groups/CharacterBlock.vue";
import {computed, ref} from "vue";
import {game_images} from "@/constants/gameImages";

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
const emit = defineEmits(['showDrawer'])

const characters = computed(() => [...props.group.characters, ...props.group.members])
const displaySubgroups = computed(() => props.group.subgroups.filter(
        s => s.characters.length + s.members.length + s.subgroups.length > 0
    )
)
const phoneScreen = ref(window.innerWidth < 768)
const updateWidth = () => {
  phoneScreen.value = window.innerWidth < 768
}
const onLeave = () => {
  window.removeEventListener('resize', updateWidth);
  window.removeEventListener('beforeunload', onLeave);
}
window.addEventListener('resize', updateWidth)
window.addEventListener('beforeunload', onLeave)
</script>
