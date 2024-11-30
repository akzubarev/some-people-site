<template class="relative">
  <img class="absolute h-[300px] w-full bg-cover" :src="game_images[game_alias].header"/>
  <div class="absolute z-0 top-20 left-[2.5%] w-[20%] h-full bg-bg-transparent-white"/>
  <div class="absolute z-0 top-20 left-[25%] w-[57.5%] h-full bg-bg-transparent-white"/>
  <div class="absolute z-0 top-20 right-[2.5%] w-[12.5%] h-full bg-bg-transparent-white"/>
  <div class="flex flex-row bg-whales-bg p-header gap-[5%] h-screen px-[2.5%]">
    <GroupNamesDrawer class="pt-6 pl-3 lg:pl-12 z-10 w-[22.5%]" :game_alias="game_alias"
                      :family_groups="family_groups" :group_groups="group_groups"/>
    <div id="groups_scrollview" v-if="group_groups"
         class="flex flex-col py-12 px-6 gap-large w-full overflow-y-scroll scroll-auto no-scrollbar z-10">
      <GroupBlock
          :key="group" :game_alias="game_alias" :group="group"
          v-for="group in family_groups.filter(g=>!groupIsEmpty(g))"
      />
      <GroupBlock
          :key="group" :game_alias="game_alias" :group="group"
          v-for="group in group_groups.filter(g=>!groupIsEmpty(g))"
      />
    </div>
  </div>
</template>


<script setup lang="ts">
import {computed} from "vue"
import gamesService from "@/services/gamesService";
import GroupBlock from "@/views/games/roles/groups/GroupBlock.vue";
import GroupNamesDrawer from "@/views/games/roles/GroupNamesDrawer.vue";
import router from "@/router";
import {useStore} from "vuex";
import {game_images} from "@/constants/gameImages";

const store = useStore()
const props = defineProps(['game_alias'])
const user = store.getters['auth/user']

const game = computed(() => store.getters['games/games'][props.game_alias])
const groups = computed(() => store.getters['games/groups'])

if (!user.mg && !game.value.open_character_list)
  router.push(`/game/${props.game_alias}/about`)

gamesService.groups(props.game_alias).then(({data}) => {
  store.dispatch('games/setGroups', data)
})

const getGroups = (family) => {
  const main_group = groups.value.find(group => group.family == family)
  if (!main_group)
    return []
  const subgroups = main_group.subgroups
  main_group.subgroups = []
  return subgroups.concat(main_group)
}

const family_groups = computed(() => getGroups(true))
const group_groups = computed(() => getGroups(false))
const groupIsEmpty = (group) => group.characters.length + group.members.length + group.subgroups.length == 0
//
// function scrollToHashElement() {
//   if (!window.location.href.includes('#'))
//     return
//   const hash = window.location.href.split("#")[1]
//   // scrollElement.scrollIntoView({behavior: "smooth"})
//   console.log(hash)
//   const scrollDiv = document.querySelector("#groups_scrollview");
//   console.log(scrollDiv)
//   if (!!scrollDiv && !!hash) {
//     const scrollElement = scrollDiv.querySelector("#" + hash)
//     console.log(scrollElement)
//     if (scrollElement) {
//       let scrollDivRect = scrollDiv.getBoundingClientRect()
//       let idRect = scrollElement.getBoundingClientRect()
//       scrollDiv.scrollBy({top: idRect.y - scrollDivRect.y, behavior: "smooth"})
//     }
//   }
// }
//
// onMounted(() => {
//   scrollToHashElement();
// })
// onhashchange = (event) => scrollToHashElement();

</script>
