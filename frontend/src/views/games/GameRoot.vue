<template>
  <router-view></router-view>
</template>

<script setup lang="ts">
import {useStore} from "vuex";

const store = useStore()
const props = defineProps(["game_alias"])

</script>
