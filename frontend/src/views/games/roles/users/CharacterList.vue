<template>
  <div class="flex flex-col gap-3">
    <CharacterFilter
        @change="(search, tag) => searchCharacters(search,tag)"
        :game_alias="game_alias"
    />
    <div class="card p-3">
      <div class="text-xl p-3">
        Персонажи
      </div>
      <div class="flex flex-col p-3 gap-6">
        <CharacterBlock
            v-for="character in characters" :key="character"
            :character="character" :game_alias="game_alias"/>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import {computed, ref, watch} from "vue"
import gamesService from "@/services/gamesService";
import CharacterBlock from "@/views/games/roles/groups/CharacterBlock.vue";
import CharacterFilter from "@/views/games/roles/users/CharacterFilter.vue";
import router from "@/router";
import {useStore} from "vuex";

const store = useStore()
const props = defineProps(["game_alias"])
const user = store.getters['auth/user']
const game = computed(() => store.getters['games/games'][props.game_alias])
const characters = ref([])

if (!user.mg && game.value && !game.value.open_character_list)
    router.push(`/game/${props.game_alias}/about`)
watch(() => props.game_alias, async alias => {
  characters.value = []
  try {
    const {data} = await gamesService.characters(alias)
    if (props.game_alias === alias) characters.value = data
  } catch {
    if (props.game_alias === alias) router.replace(`/game/${alias}/about`)
  }
}, {immediate: true})

const searchCharacters = (search, tag) => {
  gamesService.characters(props.game_alias, search, tag).then(({data}) => {
    characters.value = data
  })
}

</script>
