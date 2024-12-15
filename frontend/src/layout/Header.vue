<template>
  <Drawer :show-drawer="showDrawer" @close="showDrawer=false">
    <Menu :horizontal="false" class="pl-3" @close-drawer="showDrawer=false"/>
  </Drawer>
  <div class="absolute w-full bg-bg-transparent p-1 mt-6 z-40">
    <div class="flex flex-row w-full gap-small justify-between items-center h-8 md:h-12 md:pl-10 md:pr-3">
      <inline-svg
          class="h-8 w-8 mr-3 md:hidden cursor-pointer" @click="showDrawer=true"
          :src="require('@/assets/images/icons/common/menu.svg')"
      />
      <TitleText class="text-content-accent hover:text-content-primary"/>
      <Menu :horizontal="true" class="hidden md:flex"/>
      <Avatar
          class="h-14 w-14 md:h-20 md:w-20 md:ml-[5%] cursor-pointer"
          :src="user.avatar" @click="$router.push('/account/whales/application')"
      />
    </div>
  </div>
</template>


<script setup>
import {computed, ref} from 'vue'
import Drawer from "@/layout/Drawer.vue";
import Menu from "@/layout/Menu.vue";
import store from "@/store";
import Avatar from "@/components/Avatar.vue";
import TitleText from "@/layout/TitleText.vue";
import GroupNamesDrawer from "@/views/games/roles/GroupNamesDrawer.vue";

const user = computed(() => store.getters["auth/user"])

const showDrawer = ref(false)
</script>
