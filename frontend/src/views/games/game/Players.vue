<template>
  <div class="flex flex-col gap-3">
    <div class="card p-6">
      <div class="flex flex-row justify-between">
        <div class="text text-xl text-center w-[30%]"> Игрок</div>
        <div class="text text-xl text-center  w-[30%]"> Персонаж
        </div>
        <div class="text text-xl text-center  w-[30%]"> Заявка</div>
      </div>
      <hr>
      <div class="flex flex-col gap-6 py-3">
        <UserBlock
            v-for="user in users" :key="user" :user="user"
            :game="game_alias" :questions="questions"
        >
          <CharacterBlock
              v-if="user.applications[game_alias].character"
              :character="characters.find(c => c.id===user.applications[game_alias].character)"
              :full="false"
          />
        </UserBlock>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import {ref} from "vue"
import UserBlock from "@/views/games/UserBlock.vue";
import usersService from "@/services/usersService";
import gamesService from "@/services/gamesService";
import CharacterBlock from "@/views/games/groups/CharacterBlock.vue";
import router from "@/router";
import {useStore} from "vuex";

const store = useStore()
const characters = ref([])
const users = ref([])
const questions = ref(10)
const props = defineProps(["game_alias"])
const user = store.getters['auth/user']

gamesService.game(props.game_alias).then(({data}) => {
  if (!user.mg && !data.open_character_list)
      router.push(`/game/${props.game_alias}/about`)
})
gamesService.questions(props.game_alias).then(({data}) => {
  questions.value = data.length
})
gamesService.characters(props.game_alias).then(({data}) => {
  characters.value = data
  usersService.players(props.game_alias).then(({data}) => {
    users.value = data
  })
})


</script>
