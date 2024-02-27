<template>
      <div
        class="InfoCarousel mb-5"
        v-for="(info, i) in [projectInfo, productsInfo]"
        :key="`upper-info-${i}`"
      >
        <Carousel :items="info" :id="i" :key="`carousel-cm-${i}`" />
      </div>

    <div class="mt-5 InfoCarousel lg:col-span-2">
      <Carousel :items="marketingPlans" />
    </div>
</template>

<style lang="scss">
.InfoCarousel {
  margin: 0 -12px;
  cursor: grab;
  @media (min-width: 992px) {
    margin: 0;
  }
  .text-block {
    white-space: pre-line;
  }
  .carousel {
    text-align: left;
  }
  .carousel__pagination {
    padding: 0;
  }
  .carousel__viewport {
    height: calc(100% - 22px);
  }
  .carousel__track {
    height: 100%;
  }
  .carousel__slide {
    height: 100%;
  }
  .carousel__pagination-button {
    &:after {
      background-color: #777777;
    }
    &:hover:after {
      background-color: #ffffff;
    }
    &--active:after {
      background-color: #ffffff;
    }
  }
}
</style>

<script setup>
import { defineComponent } from "vue"
import { useI18n } from "vue-i18n"
import Carousel from "./Carousel.vue"


const t = useI18n().t
const projectInfo = [
  {
    title: "Residual Technology",
    description: t("main.residualTechDescription")
  },
  {
    title: t("main.missionTitle"),
    description: t("main.mission")
  },
  {
    title: t("main.mainTitle"),
    description: t("main.mainText")
  },
    {
    title: "Residual Community",
    description: t("main.residual")
  },
]
const productsInfo = [
    {
    title: "Residual Finance",
    description: t("main.subprojects.residualInvest"),
    tags: [
      { title: t("main.subprojects.product"), color: "#ff9e03" },
    ]
  },
  {
    title: "Residual Business",
    description: t("main.subprojects.business"),
    tags: [
      { title: t("main.subprojects.product"), color: "#ff9e03" }
    ]
  },
    {
    title: "Residual Spiritual",
    description: t("main.subprojects.spiritual"),
    tags: [
      { title: t("main.subprojects.product"), color: "#ff9e03" },
    ]
  },
  {
    title: "Residual Academy",
    description: t("main.subprojects.academy"),
    tags: [
      { title: t("main.subprojects.product"), color: "#ff9e03" },
      // { title: t("common.status.inContentDevelopment"), color: "#abc" }
    ]
  },
  {
    title: "Magic Gem",
    description: t("main.subprojects.magicGem"),
    tags: [
      { title: t("main.subprojects.product"), color: "#ff9e03" },
        // { title: t("common.status.inDevelopment"), color: "#abc" }
    ]
  },
  {
    title: "RSD Token",
    description: t("main.subprojects.rsdtoken"),
    tags: [
      { title: t("main.subprojects.product"), color: "#ff9e03" },
    ]
  },
]

const marketingPlans = [
  {
    title: "Matrix Evolution",
    description: t("main.subprojects.matrixEvolution"),
    tags: [
      { title: t("main.subprojects.marketing"), color: "#abc" },
    ]
  },
  {
    title: "Just Classic",
    description: t("main.subprojects.unilevel"),
    tags: [
      { title: t("main.subprojects.marketing"), color: "#abc" },
    ]
  },

]
</script>
