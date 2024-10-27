<template>
  <div class="flex flex-col gap-3 p-6 bg-bg-transparent rounded-xl">
    <div class="flex flex-row gap-3 items-center justify-between">
      <div class="w-full text-content-primary text-center">Игра</div>
      <hr class="h-3 w-2 bg-gray-200 border-0 rounded">
      <div class="w-full text-content-primary text-center">Персонаж</div>
      <hr class="h-3 w-2 bg-gray-200 border-0 rounded">
      <div class="w-full text-content-primary text-center">Статус</div>
      <hr class="h-3 w-2 bg-gray-200 border-0 rounded">
      <div class="w-full text-content-primary text-center">Перейти</div>
    </div>
    <hr class="h-0.5 w-full bg-gray-200 border-0 rounded">
    <div v-for="application in applications" :key="application"
         class="flex flex-col gap-1">
      <div class="flex flex-row gap-3 items-center justify-between">
        <div class="w-full text-content-primary text-center">{{ application.game?.title }}</div>
        <hr class="h-3 w-2 bg-gray-200 border-0 rounded">
        <div class="w-full text-content-primary text-center">
          {{
            application.character?.name || "Не указан"
          }}
        </div>
        <hr class="h-3 w-2 bg-gray-200 border-0 rounded">
        <div class="w-full text-content-primary text-center">
          {{
            {
              "pending": "Подана",
              "discussing": "Обсуждается",
              "confirmed": "Принята",
              "declined": "Отклонена",
              "deleted": "Удалена"
            }[application.status] || "Не подана"
          }}
        </div>
        <hr class="h-3 w-2 bg-gray-200 border-0 rounded">
        <inline-svg
            class="w-full text-content-primary text-center cursor-pointer h-8"
            @click="$router.push(`/game/${application.game.alias}/apply`)"
            :src="require('@/assets/images/icons/account/apply.svg')"/>
      </div>
      <hr class="h-0.5 w-full bg-gray-200 border-0 rounded">
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, ref} from "vue"
import {useStore} from "vuex"
import gamesService from "@/services/gamesService";

const store = useStore()
const user = computed(() => store.getters["auth/user"])

const applications = ref([])

gamesService.games({}).then(({data}) => {
  const games = data
  gamesService.applications(user.value.id).then(({data}) => {
    applications.value = data.map(application => {
      return {
        ...application,
        "game": games.find(g => g.id == application.game)
      }
    })
    console.log(applications.value)
  })
})
</script>
