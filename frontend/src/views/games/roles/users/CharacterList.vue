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
            :character="character">
          <UserBlock
              v-if="character.player" :user="character.player"
              :game="game_alias" :full="false"
          />
          <div v-else
               class="px-2 border border-1 rounded-xl text-md text-gray-500 border-gray-500">
            {{ character.applications.length }} заявок
          </div>
        </CharacterBlock>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import {ref} from "vue"
import gamesService from "@/services/gamesService";
import CharacterBlock from "@/views/games/roles/groups/CharacterBlock.vue";
import UserBlock from "@/views/games/roles/users/UserBlock.vue";
import CharacterFilter from "@/views/games/roles/users/CharacterFilter.vue";
import router from "@/router";
import {useStore} from "vuex";

const store = useStore()
const props = defineProps(["game_alias"])
const user = store.getters['auth/user']
const game = store.getters['games/game']
const characters = ref([])

if (!user.mg && !game.open_character_list)
    router.push(`/game/${props.game_alias}/about`)
gamesService.characters(props.game_alias).then(({data}) => {
  characters.value = data
})

const searchCharacters = (search, tag) => {
  gamesService.characters(props.game_alias, search, tag).then(({data}) => {
    characters.value = data
  })
}

</script>
