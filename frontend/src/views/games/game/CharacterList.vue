<template>
  <div class="flex flex-col gap-3">
    <CharacterFilter
        @change="(search, tag) => searchCharacters(search,tag)"
        :alias="alias"
    />
    <div class="card p-3">
      <div class="text text-xl text-content-primary p-3">
        Персонажи
      </div>
      <div class="flex flex-col p-3 gap-6">
        <CharacterBlock
            v-for="character in characters" :key="character"
            :character="character">
          <UserBlock
              v-if="character.player" :user="character.player"
              :game="alias" :full="false"
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


<script setup>
import {ref} from "vue"
import gamesService from "@/services/gamesService";
import CharacterBlock from "@/views/games/groups/CharacterBlock.vue";
import UserBlock from "@/views/games/UserBlock.vue";
import CharacterFilter from "@/views/games/game/CharacterFilter.vue";
import router from "@/router";
import {useStore} from "vuex";

const store = useStore()
const props = defineProps(["alias"])
const user = store.getters['auth/user']
const characters = ref([])

gamesService.game(props.alias).then(({data}) => {
  if (!user.mg && !data.open_character_list)
    router.push(`/game/${props.alias}/about`)
})
gamesService.characters(props.alias).then(({data}) => {
  characters.value = data
})

const searchCharacters = (search, tag) => {
  gamesService.characters(props.alias, search, tag).then(({data}) => {
    characters.value = data
  })
}

</script>
