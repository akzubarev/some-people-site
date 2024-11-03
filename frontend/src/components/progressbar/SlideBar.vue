<template>
  <div>
    <ProgressBar
        :color="color" class="!h-[4px]" :progress="(progress / max) * 100"
    />
    <div class="ml-2 mt-3 flex">
      <button
          @click="progress = Math.max(progress-interval,min); $emit('change', progress)"
          class="px-4 border text-xl border-teal-600 border-r-0 text-teal-600 hover:bg-teal-600 hover:rounded-l focus:outline-none focus:shadow-outline"
      >-
      </button>
      <span
          class="px-4 border text-xl border-teal-600 text-teal-600 hover:bg-teal-600 hover:focus:outline-none focus:shadow-outline"
      >
            <slot></slot>
          </span>
      <button
          @click="progress = Math.min(progress+interval,max); $emit('change', progress)"
          class="px-4 border text-xl border-teal-600 border-l-0 text-teal-600 hover:bg-teal-600 hover:rounded-r focus:outline-none focus:shadow-outline"
      >+
      </button>
    </div>
  </div>

<!--  <VueSlideBar-->
<!--      v-model="progress" :min="min" :max="max"-->
<!--      :process-style="{ backgroundColor: '&#45;&#45;accent-color-end' }"-->
<!--      :tooltipStyles="{ backgroundColor: '&#45;&#45;accent-color-end', borderColor: '&#45;&#45;accent-color-end' }">-->

<!--  </VueSlideBar>-->
</template>

<script setup>
import {ref} from 'vue'
import ProgressBar from "@/components/progressbar/ProgressBar.vue";
import tailwindConfig from "@/utils/tailwindConfig";

// import VueSlideBar from 'vue-slide-bar'

const props = defineProps({
  value: {type: Number, default: 0},
  min: {type: Number, default: 0},
  max: {type: Number, default: 100},
  interval: {type: Number, default: 1},
  color: {type: String, default: tailwindConfig.theme.colors.accent.emerald}
})
const emit = defineEmits(['change'])

const progress = ref(props.value)
</script>

