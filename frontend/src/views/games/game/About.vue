<template>
  <ActionModal
      v-if="showLocked" type="lock"
      @close="() => {showLocked = false}"
      @submit="() => {showLocked = false}"
      :title="lockedText" :buttonText="$t('common.actions.ok')">
  </ActionModal>
  <div class="flex flex flex-col gap-6 justify-end bg-cover h-full w-full min-h-full"
       :style="`background-image: url('${game_images[game_alias].background}')`">
    <div class="text-8xl font-semibold uppercase px-12"> {{ game.title }}</div>
    <div class="flex flex-col mb-12 bg-bg-transparent-2 pl-12 pr-6">
      <div class="flex flex-row gap-6 py-6 justify-between">
        <div class="flex flex-row gap-24 w-3/5">
          <div class="flex flex-col gap-3 w-1/2">
            <div class="text-xl whitespace-pre-wrap"> {{ game.short_description }}</div>
            <div class="flex flex-row gap-2">
              <div v-for="data in gameData" :key="data"
                   class="bg-content-disabled-transparent text-md text-center w-full p-3 rounded-sm">
                {{ data }}
              </div>
            </div>
          </div>
          <div class="flex flex-col gap-3 w-1/2 justify-center">
            <div v-for="link in links" :key="link" @click="link.locked ? lockedSection(link.lockedText) : link.link()"
                 class="flex flex-row gap-1 text-4xl uppercase font-semibold items-center cursor-pointer"
                 :class="link.locked ? 'text-content-disabled' : 'hover:text-content-accent'">
              {{ link.title }}
              <inline-svg v-if="link.locked" class="h-6 w-6 text-content-disabled"
                          :src="require('@/assets/images/icons/common/lock.svg')"/>
            </div>
          </div>
        </div>
        <div class="flex flex-row text-content-disabled gap-1 text-xl text-right items-center cursor-pointer"
             @click="lockedSection('Раздел в разработке.')">
          Какие-то<br> игры
          <inline-svg class="h-12 w-12" :src="require('@/assets/images/icons/common/arrow.svg')"/>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import {computed, ref} from "vue"
import gamesService from "@/services/gamesService";
import ActionModal from "@/components/ActionModal.vue";
import {useStore} from "vuex";
import {useRouter} from "vue-router";
import {game_images} from "@/constants/gameImages";
import {formatDateRange} from "@/utils/dates";

const store = useStore()
const router = useRouter()
const props = defineProps(['game_alias'])
const user = store.getters['auth/user']
const showLocked = ref(false)
const lockedText = ref('Раздел в разработке')

const lockedSection = (text) => {
  lockedText.value = text
  showLocked.value = true
}
const game = ref({
  id: 1,
  alias: 'lorem ipsum',
  title: "lorem ipsum",
  image: null,
  vk: "",
})
gamesService.game(props.game_alias).then(({data}) => {
  game.value = data
})

const gameData = computed(() => [
  `${formatDateRange(new Date(game.value.start), new Date(game.value.end))} ${game.value.year}`,
  game.value.location, `${game.value.player_count} чел`,
])

const links = computed(() => {
  return [
    {
      link: () => router.push(`/game/${game.value.alias}/apply`),
      locked: !user.mg && !game.value.open_applications,
      lockedText: 'Заявки еще/уже не принимаются',
      title: 'Заявка',
    },
    {
      link: () => router.push(`/game/${game.value.alias}/roles`),
      locked: !user.mg && !game.value.open_character_list,
      lockedText: "Сетка ролей еще не открыта",
      title: 'Сетка ролей',
    },
    {
      link: () => window.open(game.value.vk, '_blank').focus(),
      title: 'Группа ВК',
    },
  ]
})

const otherGames = () => window.open(
    `/game/${{'whales': 'frostpunk', 'frostpunk': 'whales'}[props.game_alias]}/about`,
    '_blank'
).focus();
</script>
