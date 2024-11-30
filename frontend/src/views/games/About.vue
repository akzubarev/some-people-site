<template>
  <ActionModal
      v-if="showLocked" type="lock" :title="lockedText"
      @close="() => {showLocked = false}"
      @submit="() => {showLocked = false}">
  </ActionModal>
  <div class="flex flex flex-col gap-medium justify-end bg-cover h-full w-full min-h-full bg-left-bottom"
       :style="`background-image: url('${game_images[game_alias].background}')`">
    <div class="text-largest font-semibold uppercase px-12"> {{ game.title }}</div>
    <div class="flex flex-row gap-medium py-6 mb-12 bg-bg-transparent-2 pl-12 pr-3 justify-between">
      <div class="flex flex-row gap-[5%]">
        <div id="description" class="flex flex-col gap-small w-[45%]">
          <div class="sm:text-base lg:text-xl whitespace-pre-wrap"> {{ game.short_description }}</div>
          <div id="ags" class="flex flex-row gap-2">
            <div v-for="data in gameData" :key="data"
                 class="sm:text-sm md:text-lg lg:text-xl p-1 lg:p-2 bg-content-disabled-transparent text-center w-full rounded-sm">
              {{ data }}
            </div>
          </div>
        </div>
        <div id="links" class="flex flex-col gap-[7.5%] justify-center">
          <div v-for="link in links" :key="link" @click="link.locked ? lockedSection(link.lockedText) : link.link()"
               class="flex flex-row gap-xs text-large uppercase font-semibold items-center cursor-pointer"
               :class="link.locked ? 'text-content-disabled' : 'hover:text-content-accent'">
            {{ link.title }}
            <inline-svg v-if="link.locked" class="h-6 w-6 text-content-disabled"
                        :src="require('@/assets/images/icons/common/lock.svg')"/>
          </div>
        </div>
        <inline-svg v-if="game_images[game_alias].logo" class="h-full" :src="game_images[game_alias].logo"/>
      </div>
      <div @click="otherGames()"
           class="flex flex-row gap-xs text-medium text-right items-center
           w-[15%] min-w-[150px] justify-end cursor-pointer">
        Какие-то<br>игры
        <inline-svg class="h-12 w-12" :src="require('@/assets/images/icons/common/arrow.svg')"/>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import {computed, ref} from "vue"
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
const lockedText = ref('')


const game = computed(() => store.getters['games/games'][props.game_alias])
const gameData = computed(() => [
  `${formatDateRange(new Date(game.value.start), new Date(game.value.end))} ${game.value.year}`,
  game.value.location, `${game.value.player_count} чел`,
])

const links = computed(() => [
  {
    link: () => router.push(`/account/${props.game_alias}/application`),
    locked: !user.mg && !game.value.open_applications,
    lockedText: 'Заявки еще/уже не принимаются',
    title: 'Заявка',
  },
  {
    link: () => router.push(`/game/${props.game_alias}/roles`),
    locked: !user.mg && !game.value.open_character_list,
    lockedText: "Сетка ролей еще не открыта",
    title: 'Сетка ролей',
  },
  {
    link: () => window.open(game.value.vk, '_blank').focus(),
    title: 'Группа ВК',
  },
])
const lockedSection = (lockedSectionText) => {
  lockedText.value = lockedSectionText
  showLocked.value = true
}

const otherGames = () => router.push(`/game/${{'whales': 'frostpunk', 'frostpunk': 'whales'}[props.game_alias]}/about`)
</script>
