<template>
  <div class="w-full m-auto min-h-screen relative bg-bg-primary">
    <Header />
    <PageState v-if="$route.meta.requiresGames && gamesError" :message="gamesError" retry />
    <PageState v-else-if="$route.meta.requiresGames && !hasGames" message="Пока нет доступных игр." />
    <PageState v-else-if="$route.meta.requiresAccount && accountError" :message="accountError" retry />
    <router-view v-else />
  </div>
</template>
<script setup>
import {computed} from 'vue'
import {useStore} from 'vuex'
import Header from '@/layout/Header.vue'
import PageState from '@/components/PageState.vue'
const store = useStore()
const gamesError = computed(() => store.state.games.gamesError)
const accountError = computed(() => store.state.games.accountError)
const hasGames = computed(() => Object.keys(store.getters['games/games']).length > 0)
</script>
