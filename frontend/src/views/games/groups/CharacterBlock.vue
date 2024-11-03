<template>
  <div class="flex flex-col gap-2 w-full">
    <div class="flex flex-row items-center gap-4">
      <img
          class="z-30 w-[200px] h-[200px] rounded-full"
          :src="character.image || characters[game][character.id] || characters[game]['default']"
      />
      <div class="flex flex-col w-fit gap-1 items-start">
        <div class="flex flex-row text-lg text-content-primary whitespace-pre-wrap">
              <span class="text-xl text-content-primary">{{
                  character.name
                }} — </span> <span class="text-xl text-content-primary cursor-pointer">{{
            character.player ? character.player.name : "Свободная роль"
          }}  </span>
        </div>
        <div class="flex flex-row items-center gap-4 p-3 bg-gray-800 bg-opacity-60 rounded-lg -ml-14 z-20" v-if="full">
          <div class=" text-sm text-content-primary whitespace-pre-wrap ml-14">
            {{ character.description }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>

import {ref} from "vue";
import {characters} from "@/constants/characterImages";

const props = defineProps({
  character: {
    id: 1,
    master: 1,
    name: "lorem ipsum",
    description: "lorem ipsum",
    image: null,
    status: "active",
    applications: [],
    player: {}
  },
  full: {type: Boolean, default: true},
  game: {type: String,}
})
const character = ref({
  ...props.character,
  status: "no",
})
</script>