<template>
  <div class="flex flex-col gap-2 w-full">
    <div class="flex flex-row items-center gap-4">
      <img class="z-30 w-[100px] h-[100px] rounded-full" :src="master.image"/>
      <div
          class="flex flex-col w-fit gap-1 items-start">
        <div
            class="flex flex-row text-lg whitespace-pre-wrap">
              <span class="text-xl">{{
                  master.name
                }} — </span> <span class="text-xl cursor-pointer">{{
            master.status
          }}  </span>
        </div>
        <div
            class="-ml-14 z-20 flex flex-row items-center gap-4 p-3 bg-gray-800 bg-opacity-60 rounded-lg">
          <div class="ml-14 text-sm whitespace-pre-wrap">
            {{ master.description }}
          </div>
        </div>
      </div>
    </div>
    <Footer/>
  </div>
</template>


<script setup lang="ts">


import About from "@/views/games/About.vue";
import Footer from "@/layout/Footer.vue";

const props = defineProps({
  master: {
    name: "lorem ipsum",
    description: "lorem ipsum",
    image: null,
    status: "ГМ",
  },
})
</script>