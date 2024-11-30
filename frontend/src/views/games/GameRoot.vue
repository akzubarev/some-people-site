<template>
  <router-view></router-view>
</template>

<script setup lang="ts">
import {computed} from "vue";
import {useStore} from "vuex";
import {defaultGame} from "@/constants/common"

const store = useStore()
const user = store.getters['auth/user']
const props = defineProps(["game_alias"])
const game = computed(()=>store.getters['games/games'][props.game_alias])

const menuConfig = computed(() => {
  return [
    {
      link: `/game/${game.value.alias}/about`,
      locked: false,
      title: "Описание",
    },
    {
      link: `/game/${game.value.alias}/roles`,
      locked: !user.mg && !game.value.open_character_list,
      lockedText: "Сетка ролей еще не открыта",
      title: "Сетка ролей",
    },
    {
      link: `/game/${game.value.alias}/characters`,
      locked: !user.mg && !game.value.open_character_list,
      lockedText: "Сетка ролей еще не открыта",
      title: "Список персонажей",
    },
    {
      link: `/game/${game.value.alias}/apply`,
      locked: !user.mg && !game.value.open_applications,
      lockedText: "Заявки еще/уже не принимаются",
      title: "Заявка",
    },
    {
      link: `/game/${game.value.alias}/players`,
      locked: !user.mg && !game.value.open_character_list,
      lockedText: "Сетка ролей еще не открыта",
      title: "Игроки",
    },
  ]
})
</script>
