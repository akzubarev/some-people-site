<template>
  <div class="flex flex-col gap-5">
    <div class="flex flex-row justify-center">
      <div class="text-4xl"> МГ «Какие-то Люди»</div>
    </div>
    <!--    <ImageBanner-->
    <!--        class="h-[500px]"-->
    <!--        :image="require('@/assets/images/background.png')"-->
    <!--        title="Фростпанк" description="Описание описание описание"-->
    <!--        :tags="['Раз' , 'Два','Три']" :full="false"-->
    <!--        :buttons="[{text: 'Подробнее', href:`/game/frostpunk/about`}]"-->
    <!--    />-->
    <div class="grid gap-4 grid-cols-2 lg:grid-cols-4 mt-6">
      <DashboardCard text="Игры" route="/games">
        <inline-svg
            :src="require('@/assets/images/icons/dashboard/book.svg')"/>
      </DashboardCard>
    </div>
  </div>
</template>

<script setup>
import DashboardCard from "@/views/dashboard/DashboardCard.vue";
// import ImageBanner from "@/views/dashboard/ImageBanner.vue";


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
