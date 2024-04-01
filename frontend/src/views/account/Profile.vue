<template>
  <div
      class="flex flex-col p-6 gap-6 rounded-xl bg-gray-700 bg-opacity-60 mt-48 mx-3">
    <div
        class="flex max-md:flex-col max-md:justify-center items-center gap-6 relative">
      <Avatar
          class="min-w-[128px]" size="128" :src="user.avatar"
          :username="user.first_name + ' ' + user.last_name"
      ></Avatar>
      <div class="flex flex-col gap-1 max-md:items-center justify-center">
        <span class="text-2xl">
          {{ user.first_name }} {{ user.last_name }} | {{ user.username }}
        </span>
        <span class="text-normal text-gray-400">{{ user.email }}</span>
      </div>
      <button
          @click="$router.push('/account/settings')"
          class="btn bg-gray-800 text-white max-md:w-full flex gap-2 justify-center md:absolute top-6 right-6">
        <inline-svg
            :src="require('@/assets/images/icons/common/Settings.svg')"/>
        {{ $t("menu.settings") }}
      </button>
    </div>
    <div class="flex flex-col gap-3 p-6 bg-[--bg-card] rounded-xl ">
      <div class="flex flex-row gap-3 items-center justify-between">
        <div class="w-full text-center">Игра</div>
        <hr class="h-3 w-2 bg-gray-200 border-0 rounded">
        <div class="w-full text-center">Персонаж</div>
        <hr class="h-3 w-2 bg-gray-200 border-0 rounded">
        <div class="w-full text-center">Статус</div>
        <hr class="h-3 w-2 bg-gray-200 border-0 rounded">
        <div class="w-full text-center">Перейти</div>
      </div>
      <hr class="h-0.5 w-full bg-gray-200 border-0 rounded">
      <div v-for="application in applications" :key="application"
           class="flex flex-col gap-1">
        <div class="flex flex-row gap-3 items-center justify-between">
          <div class="w-full text-center">{{ application.game?.title }}</div>
          <hr class="h-3 w-2 bg-gray-200 border-0 rounded">
          <div class="w-full text-center">
            {{
              application.character?.name || "Не указан"
            }}
          </div>
          <hr class="h-3 w-2 bg-gray-200 border-0 rounded">
          <div class="w-full text-center">
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
              class="w-full text-center cursor-pointer h-8"
              @click="$router.push(`/game/${application.game.alias}/apply`)"
              :src="require('@/assets/images/icons/common/enter.svg')"/>
        </div>
        <hr class="h-0.5 w-full bg-gray-200 border-0 rounded">
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted, ref} from "vue"
import {useStore} from "vuex"
import {useI18n} from "vue-i18n"
import Avatar from "@/components/avatar";
import {Tooltip} from "bootstrap";
import gamesService from "@/services/gamesService";
import s from "@/components/filters/styles.module.scss";


const {t} = useI18n()
const store = useStore()
const user = computed(() => store.getters["auth/user"])

onMounted(() => {
  const tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
  )
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new Tooltip(tooltipTriggerEl)
  })
})

const games = ref([])
const applications = ref([])

gamesService.games({}).then(({data}) => {
  games.value = data
  gamesService.applications(user.value.id).then(({data}) => {
    applications.value = data.map(application => {
      return {
        ...application,
        "game": games.value.find(g => g.id == application.game)
      }
    })
    console.log(applications.value)
  })
})
</script>
