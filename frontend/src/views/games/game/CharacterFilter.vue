<template>
  <div class="card flex flex-col w-full p-3 gap-3">
    <Field
        class="form-control form-control-lg form-control-solid"
        type="text" :name="search" placeholder="Поиск по персонажам"
        v-model="search" @change="$emit('change', search, selectedTag)"
    />
    <div class="flex flex-row w-full gap-1 p-3">
      <div class="text-md mr-3">Тэги:</div>
      <Tag v-for="tag in tags" :key="tag"
           @click="()=>{selectedTag=tag.name; $emit('change', search, selectedTag)}"
           :text="tag.name" :color="tag.color"
           :selected="selectedTag===tag.name"
      />
    </div>
  </div>
</template>

<script setup lang="ts">

import {Field} from "vee-validate";
import {ref} from "vue";
import gamesService from "@/services/gamesService";
import Tag from "@/views/games/Tag.vue";

const props = defineProps(["alias"])
const emit = defineEmits(["change"])

const tags = ref([])
gamesService.tags(props.alias).then(({data}) => {
  tags.value = data
})

const search = ref("")
const selectedTag = ref("")

</script>
