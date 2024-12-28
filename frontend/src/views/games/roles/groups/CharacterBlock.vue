<template>
  <div class="flex flex-col py-2 px-[5%] md:py-0 md:px-0 md:flex-row justify-between md:gap-[4%]
   bg-bg-transparent-white md:bg-transparent">
    <div v-if="phoneScreen && !personal" class="flex flex-col w-full mb-1">
      <div class="text-xs text-content-secondary"> {{ character.alias }}</div>
      <div class="flex flex-row justify-between w-full">
        <div class="text-medium font-semibold text-content-secondary">{{ character.name }}</div>
        <PopupWrapper v-if="character.player">
          <template #header>
            <div class="text-medium text-content-secondary sm:cursor-pointer md:cursor-default text-start">
              {{ character.player ? character.player.username : "Свободно" }}
            </div>
          </template>
          <template #content>
            <div class="flex flex-row gap-3 items-center p-1 bg-bg-transparent rounded-xl">
              <div v-if="character.player?.vk" @click="openVK(character.player.vk)"
                   class="text-medium cursor-pointer">
                VK
              </div>
              <div v-if="character.player?.telegram" @click="openTG(character.player.telegram)"
                   class="text-medium cursor-pointer">
                TG
              </div>
            </div>
          </template>
        </PopupWrapper>
        <div v-else class="text-medium text-content-secondary sm:cursor-pointer md:cursor-default text-start"
             :class="character.player ? 'underline cursor-pointer': ''">
          {{ character.player ? character.player.username : "Свободно" }}
        </div>
      </div>
    </div>
    <div class="flex flex-row gap-medium w-full md:pr-6">
      <div class="flex w-[30%] md:w-[20%]">
        <CharacterPicture :game_alias="game_alias" :src="character.image" :name="character.name_eng"/>
      </div>
      <div class="flex flex-col w-full gap-1" :class="!phoneScreen || personal ? 'items-start':'items-end'">
        <div v-if="!phoneScreen || personal" class="text-medium text-content-secondary font-semibold">
          {{ character.name }}, {{ character.alias }}
        </div>
        <div class="text-xxs md:text-sm text-content-secondary-shadowed whitespace-pre-wrap"> {{
            character.description
          }}
        </div>
        <a v-if="personal" class="text-sm font-semibold text-content-secondary whitespace-pre-wrap"
           :href="`/game/${game_alias}/roles`">
          -> Перейти в сетку
        </a>
        <PopupWrapper v-if="!user.value?.likes">
          <template #header>
            <inline-svg
                v-if="phoneScreen && !character.player && !personal" class="w-6 h-6" @click="like()"
                :src="require(`@/assets/images/icons/roles/heart-${liked ? 'filled': 'unfilled'}.svg`)"
            />
          </template>
          <template #content>
            <div class="text-sm bg-bg-transparent rounded-xl min-w-[140px] p-1">
              {{ user.id ? 'Хочу играть этого персонажа!' : 'Сначала нужно подать заявку' }}
            </div>
          </template>
        </PopupWrapper>
        <inline-svg
            v-if="user.value?.likes && phoneScreen && !character.player && !personal" class="w-6 h-6" @click="like()"
            :src="require(`@/assets/images/icons/roles/heart-${liked ? 'filled': 'unfilled'}.svg`)"
        />
      </div>
    </div>
    <div v-if="!phoneScreen && !personal" class="flex flex-col w-[17.5%] ml-[2,5%] pl-6 gap-1">
      <div class="text-medium text-content-secondary sm:cursor-pointer md:cursor-default text-start">
        {{ character.player ? character.player.username : "Свободно" }}
      </div>
      <div class="flex flex-row gap-3 items-center pr-[2.5%]">
        <div v-if="character.player?.vk" @click="openVK(character.player.vk)"
             class="text-medium text-content-secondary-shadowed cursor-pointer">
          VK
        </div>
        <div v-if="character.player?.telegram" @click="openTG(character.player.telegram)"
             class="text-medium text-content-secondary-shadowed cursor-pointer">
          TG
        </div>
        <PopupWrapper v-if="!character.player && !user.value?.likes">
          <template #header>
            <inline-svg
                class="w-6 h-6" @click="like()"
                :src="require(`@/assets/images/icons/roles/heart-${liked ? 'filled': 'unfilled'}.svg`)"
            />
          </template>
          <template #content>
            <div class="text-sm bg-bg-transparent rounded-xl min-w-[140px] p-1">
              {{ user.id ? 'Хочу играть этого персонажа!' : 'Сначала нужно подать заявку' }}
            </div>
          </template>
        </PopupWrapper>
        <inline-svg
            v-if="user.value?.likes && phoneScreen && !character.player && !personal" class="w-6 h-6" @click="like()"
            :src="require(`@/assets/images/icons/roles/heart-${liked ? 'filled': 'unfilled'}.svg`)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, ref} from "vue";
import gamesService from "@/services/gamesService";
import CharacterPicture from "@/views/games/roles/groups/CharacterPicture.vue";
import {useStore} from "vuex";
import {useRouter} from "vue-router";
import PopupWrapper from "@/components/PopupWrapper.vue";

const store = useStore()
const router = useRouter()
const props = defineProps({
  character: {
    id: 1,
    master: 1,
    alias: "lorem ipsum",
    name: "lorem ipsum",
    description: "lorem ipsum",
    image: null,
    applications: [],
    liked: false,
    player: {
      username: "lorem",
      telegram: "ipsum",
      vk: "lorem",
    }
  },
  personal: {type: Boolean, default: false},
  game_alias: {type: String,},
})
const user = computed(() => store.getters['auth/user'])
const liked = computed(() => user.value.likes?.includes(props.character.id))

const openTG = (username) => {
  window.open(`https://t.me/${username}`, '_blank').focus()
}
const openVK = (username) => {
  window.open(`https://vk.com/${username}`, '_blank').focus()
}

const like = () => {
  if (!user.value) {
    router.push('/sign-in')
    return
  }
  const userToSet = user.value
  const new_value = !liked.value
  if (new_value)
    userToSet.likes.push(props.character.id)
  else
    userToSet.likes = userToSet.likes.filter(ch_id => ch_id != props.character.id)
  gamesService.like_character(props.game_alias, props.character.id, new_value).then(({data}) => {
    store.dispatch('auth/setUser', userToSet)
  })
}
const phoneScreen = ref(window.innerWidth < 768)
const updateWidth = () => phoneScreen.value = window.innerWidth < 768
const onLeave = () => {
  window.removeEventListener('resize', updateWidth);
  window.removeEventListener('beforeunload', onLeave);
}
window.addEventListener('resize', updateWidth)
window.addEventListener('beforeunload', onLeave)
</script>