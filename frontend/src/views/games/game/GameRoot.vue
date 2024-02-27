<template>
<!--  <Menu :alias="game.alias" :config="menuConfig" :title="game.title"/>-->
  <router-view></router-view>
</template>

<script setup lang="ts">
import Menu from "@/views/games/game/Menu.vue";
import gamesService from "@/services/gamesService";
import {ref, computed} from "vue";
import {useStore} from "vuex";

const store = useStore()
const user = store.getters['auth/user']
const props = defineProps(["alias"])
const game = ref({
  id: 1,
  title: "lorem ipsum",
  alias: "loremipsum",
  factions: [],
  open_applications: false,
  open_character_list: false
})
gamesService.game(props.alias).then(({data}) => {
  game.value = data
})

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
