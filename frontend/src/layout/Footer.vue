<template>
  <div class="footer flex flex-lg-column py-1 px-3 bg-opacity-70" id="kt_footer">
    <div
        class="flex flex-col flex-md-row items-center justify-between"
        :class="{ 'container-fluid': footerWidthFluid, container: !footerWidthFluid}"
    >
      <div class="text-dark order-2 order-md-1">
        <span class="text-content-muted fw-bold me-1">&#127813; Сайт написан</span>
        <a href="https://github.com/akzubarev/some-people-site"
           target="_blank" class="text-hover-accent">@akzubarev</a>
        <span class="text-content-muted fw-bold me-1">, можете написать</span>
        <a href="https://t.me/Package_Man" target="_blank" class="text-hover-accent">мне</a>
        <span class="text-content-muted fw-bold me-1"> за исходниками</span>
      </div>
      <!--    <div class="text-dark order-2 order-md-1">-->
      <!--      <span class="text-muted fw-bold me-1">2024&copy;</span>-->
      <!--      <a href="/frontend/public" target="_blank" class="text-gray-800 text-hover-primary">-->
      <!--        maslow.me-->
      <!--      </a>-->
      <!--    </div>-->
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "vue"
import {footerWidthFluid} from "@/core/helpers/config"

export default defineComponent({
  name: "KTFooter",
  setup() {
    return {
      footerWidthFluid
    }
  }
})
</script>
