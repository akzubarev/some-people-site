<template>
  <div class="flex flex-col gap-5 mt-48">
    <div class="flex flex-row justify-center">
      <div class="text-4xl"> МГ «Какие-то Люди»</div>
    </div>
    <!--    <div class="grid gap-4 grid-cols-2 lg:grid-cols-4 mt-6">-->
    <!--      <DashboardCard text="Игры" route="/games">-->
    <!--        <inline-svg-->
    <!--            :src="require('@/assets/images/icons/dashboard/book.svg')"/>-->
    <!--      </DashboardCard>-->
    <!--    </div>-->
    <div class="flex flex-col p-3 gap-6">
      <MGBlock v-for="master in mg" :key="master" :master="master"/>
    </div>
  </div>
</template>

<script setup>
// import DashboardCard from "@/views/dashboard/DashboardCard.vue";
import usersService from "@/services/usersService";
import {ref} from "vue";
import {mgData} from "@/views/dashboard/mgData";
import MGBlock from "@/views/dashboard/MGBlock.vue";

const mg = ref([])
usersService.mg().then(({data}) => {
  mg.value = data.map(d => mgData[d.username]).sort(m => m.idx)
})

</script>


<style lang="scss">
.product-buttons {
  @apply relative flex items-end min-h-[7rem] p-4 overflow-hidden cursor-pointer;
  &.disabled {
    @apply cursor-default;
    & img {
      @apply grayscale
    }
  }
}

</style>
