<template>
  <div class="flex flex-col gap-3">
    <div class="card p-6">
      <div class="flex flex-row justify-between">
        <div class="text text-xl text-center text-white w-[30%]"> Игрок</div>
        <div class="text text-xl text-center  text-white w-[30%]"> Персонаж
        </div>
        <div class="text text-xl text-center  text-white w-[30%]"> Заявка</div>
      </div>
      <hr>
      <div class="flex flex-col gap-6 py-3">
        <UserBlock
            v-for="user in users" :key="user" :user="user"
            :game="alias" :questions="questions"
        >
          <CharacterBlock
              v-if="user.applications[alias].character"
              :character="characters.find(c => c.id===user.applications[alias].character)"
              :full="false"
          />
        </UserBlock>
      </div>
    </div>
  </div>
</template>


<script setup>
import {ref} from "vue"
import UserBlock from "@/views/games/UserBlock.vue";
import usersService from "@/services/usersService";
import gamesService from "@/services/gamesService";
import CharacterBlock from "@/views/games/factions/CharacterBlock.vue";
import router from "@/router";
import {useStore} from "vuex";

const store = useStore()
const characters = ref([])
const users = ref([])
const questions = ref(10)
const props = defineProps(["alias"])
const user = store.getters['auth/user']

gamesService.game(props.alias).then(({data}) => {
  if (!user.mg && !data.open_character_list)
      router.push(`/game/${props.alias}/about`)
})
gamesService.questions(props.alias).then(({data}) => {
  questions.value = data.length
})
gamesService.characters(props.alias).then(({data}) => {
  characters.value = data
  usersService.players(props.alias).then(({data}) => {
    users.value = data
  })
})


</script>
