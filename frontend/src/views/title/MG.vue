<template>
  <div class="flex flex-col gap-5 mt-48">
    <div class="flex flex-row justify-center">
      <div class="text-4xl"> МГ «Какие-то Люди»</div>
    </div>
    <div class="flex flex-col px-3" v-for="{title, masters} in mg" :key="title">
      <div class="text-2xl"> {{ title }}</div>
      <div class="flex flex-col p-3 gap-6">
        <MGBlock v-for="master in masters" :key="master" :master="master"/>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import usersService from "@/services/usersService";
import {ref} from "vue";
import {mgData} from "@/constants/mgData";
import MGBlock from "@/views/title/MGBlock.vue";

const mg = ref({})
usersService.mg().then(({data}) => {
  mg.value = [
    {title: "Гм'ы", masters: data.map(d => mgData[d.username]).filter(Boolean).filter(m => m.idx <= 2).sort((a, b) => a.idx - b.idx)},
    {title: "Сюжетный блок", masters: data.map(d => mgData[d.username]).filter(Boolean).filter(m => m.idx > 2).sort((a, b) => a.idx - b.idx)},
    {title: "Арт-блок", masters: []},
    {title: "Игротехи", masters: []},
  ]
})

</script>
