<template>
  <ActionModal
      v-if="showLocked" type="lock"
      @close="() => {showLocked = false}"
      @submit="() => {showLocked = false}"
      :title="lockedText" :buttonText="$t('common.actions.ok')">
  </ActionModal>
  <div class="flex flex flex-col gap-3 bg-cover h-full w-full min-h-full"
       :style="`background-image: url('${games[alias].background}')`"
  >
    <div class="flex flex-col h-full gap-3 justify-center">
      <div class="flex flex-col bg-gray-800 bg-opacity-60 px-28">
        <div class="text-[--dark-text-color] text-8xl font-bold -mt-10">
          {{ game.title }}
        </div>
        <div
            class="flex flex-row gap-28 pb-6 justify-between">
          <div class="flex flex-col gap-3 p-3 w-[40%] justify-center">
            <div
                class="text-[--dark-text-color] whitespace-pre-wrap max-w-[400px]">
              {{ game.short_description }}
            </div>
            <div class="flex flex-row gap-2">
              <div v-for="data in gameData" :key="data"
                   class="px-2 border w-fit h-fit border-1 rounded-xl text-md text-gray-500 border-gray-500">
                {{ data }}
              </div>
            </div>
          </div>
          <div class="flex flex-col gap-5 p-3 w-[40%] justify-center">
            <div v-for="link in links" :key="link"
                 @click="link.locked ? lockedSection(link.lockedText) : link.link()"
                 class="text-4xl flex flex-row gap-1 items-center cursor-pointer"
                 :class="link.locked ? 'text-gray-500' : 'hover:text-gray-300'">
              {{ link.title }}
              <inline-svg
                  v-if="link.locked" class="h-[25px] w-[25px] text-gray-500"
                  :src="require('@/assets/images/icons/common/lock.svg')"/>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import {computed, ref} from "vue"
import gamesService from "@/services/gamesService";
import ActionModal from "@/components/ActionModal.vue";
import {useStore} from "vuex";
import {useRouter} from "vue-router";
import {games} from "@/constants/gameImages";

const store = useStore()
const router = useRouter()
const props = defineProps(["alias"])
const user = store.getters['auth/user']
const showLocked = ref(false)
const lockedText = ref("Раздел в разработке")

const lockedSection = (text) => {
  lockedText.value = text
  showLocked.value = true
}
const game = ref({
  id: 1,
  title: "lorem ipsum",
  image: null,
  vk: "",
})
gamesService.game(props.alias).then(({data}) => {
  game.value = data
})
const formatDate = date => {
  return new Date(date).toLocaleDateString(
      'ru', {
        day: "numeric", month: "numeric",
        // year: "numeric", hour: "numeric", minute: "numeric"
      })
}
const gameData = computed(() => [
  `${formatDate(game.value.start)} - ${formatDate(game.value.end)} ${game.value.year}`,
  game.value.location, "99 чел.",
])

const links = computed(() => {
  return [
    {
      link: () => router.push(`/game/${game.value.alias}/apply`),
      locked: !user.mg && !game.value.open_applications,
      lockedText: "Заявки еще/уже не принимаются",
      title: "Заявка",
    },
    {
      link: () => router.push(`/game/${game.value.alias}/roles`),
      locked: !user.mg && !game.value.open_character_list,
      lockedText: "Сетка ролей еще не открыта",
      title: "Сетка ролей",
    },
    {
      link: () => window.open(game.value.vk, "_blank").focus(),
      title: "Группа вк",
    },
  ]
})
</script>
