<template>
  <ActionModal
      v-if="showLocked" type="lock" :title="lockedText"
      @close="() => {showLocked = false}"
      @submit="() => {showLocked = false}">
  </ActionModal>
  <div
      class="flex flex flex-col gap-1 md:gap-3 p-header md:justify-end bg-cover h-screen w-full bg-bottom md:bg-left-bottom"
      :style="`background-image: url('${game_images[game_alias].background}')`">
    <div class="text-largest font-bold md:font-semibold uppercase px-6 md:px-12"
         :class="game_alias == 'frostpunk' ? 'text-content-primary ': 'text-content-secondary md:text-content-primary'">
      {{ game.title }}
    </div>
    <div class="flex flex-col items-center md:flex-row h-full md:h-fit gap-medium md:py-6 md:mb-12
    md:bg-bg-transparent-2 md:pl-12 md:pr-3 justify-between md:justify-normal">
      <div id="description" class="flex flex-col gap-small w-full px-6 md:px-0 md:w-[70%]">
        <div class="text-base md:text-lg lg:text-2xl whitespace-pre-wrap"
             :class="game_alias == 'frostpunk' ? 'text-content-primary ': 'text-content-secondary md:text-content-primary'">
          {{ game.short_description }}
        </div>
        <div id="tags" class="flex flex-row gap-2">
          <div v-for="data in gameData" :key="data"
               class="flex sm:text-sm md:text-lg lg:text-xl p-1 lg:p-2
               min-h-[40px] md:min-h-none justify-center items-center bg-content-disabled-transparent text-center w-full rounded-sm"
               :class="game_alias == 'frostpunk' ? 'text-content-primary ': 'text-content-secondary md:text-content-primary'">
            {{ data }}
          </div>
        </div>
      </div>
      <div class="flex flex-col md:flex-row w-full items-center gap-large justify-between md:gap-[5%]">
        <div class="flex flex-row w-full items-center justify-between md:justify-normal md:gap-[5%]">
          <div id="links" class="flex flex-col gap-6 justify-center">
            <div v-for="link in links" :key="link" @click="link.locked ? lockedSection(link.lockedText) : link.link()"
                 class="flex flex-row p-3 pl-6 pr-12 md:!p-0 gap-xs text-large uppercase font-semibold items-center
               cursor-pointer bg-bg-transparent-2 md:bg-transparent rounded-sm"
                 :class="link.locked ? 'text-content-disabled' : 'hover:text-content-accent'">
              {{ link.title }}
              <inline-svg v-if="link.locked" class="h-6 w-6 text-content-disabled"
                          :src="require('@/assets/images/icons/common/lock.svg')"/>
            </div>
          </div>
          <inline-svg v-if="!phoneScreen && game_images[game_alias].logo"
                      :src="game_images[game_alias].logo" class="h-full"/>
          <img v-if="phoneScreen && game_images[game_alias].logo_half"
               :src="game_images[game_alias].logo_half" class="h-full"/>
        </div>
        <div id="other_games" @click="otherGames()"
             class="flex flex-row gap-xs items-center md:w-[15%] md:min-w-[150px] md:justify-end cursor-pointer">
          <div class="hidden md:flex text-medium text-right md:min-w-[84px]"> Какие-то<br>игры</div>
          <inline-svg class="h-12 w-12 rotate-90 md:rotate-0" :src="require('@/assets/images/icons/common/arrow.svg')"/>
        </div>
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


const phoneScreen = ref(window.innerWidth < 768)
const updateWidth = () => phoneScreen.value = window.innerWidth < 768
const onLeave = () => {
  window.removeEventListener('resize', updateWidth);
  window.removeEventListener('beforeunload', onLeave);
}
window.addEventListener('resize', updateWidth)
window.addEventListener('beforeunload', onLeave)
</script>
