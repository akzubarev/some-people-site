<template>
  <!--begin::Page loader-->
  <template v-if="loaderType === 'spinner-message'">
    <div class="page-loader flex-column">
      <span class="spinner-border text-primary" role="status"></span>
      <span class="text-muted fs-6 fw-bold mt-5">Loading...</span>
    </div>
  </template>
  <template v-else-if="loaderType === 'spinner-logo'">
    <div class="page-loader flex-column">
      <img alt="Logo" class="max-h-75px" :src="logo" />

      <div class="d-flex align-items-center mt-5">
        <span class="spinner-border text-primary" role="status"></span>
        <span class="text-muted fs-6 fw-bold ms-5">Loading...</span>
      </div>
    </div>
  </template>
  <template v-else-if="loaderType === 'neon-bullet'">
    <div class="page-loader flex-column">
      <SpinLoader />
    </div>
  </template>
  <template v-else>
    <div class="page-loader">
      <span class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </span>
    </div>
  </template>
  <!--end::Page Loader-->
</template>
<style scoped>
.ip {
  width: 16em;
  height: 8em;
}
.ip__track {
  stroke: hsl(var(--hue), 90%, 90%);
  transition: stroke var(--trans-dur);
}
.ip__worm1,
.ip__worm2 {
  animation: worm1 2s linear infinite;
}
.ip__worm2 {
  animation-name: worm2;
}

/* Dark theme */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: hsl(var(--hue), 90%, 5%);
    --fg: hsl(var(--hue), 90%, 95%);
  }
  .ip__track {
    stroke: hsl(var(--hue), 90%, 15%);
  }
}

/* Animation */
@keyframes worm1 {
  from {
    stroke-dashoffset: 0;
  }
  50% {
    animation-timing-function: steps(1);
    stroke-dashoffset: -358;
  }
  50.01% {
    animation-timing-function: linear;
    stroke-dashoffset: 358;
  }
  to {
    stroke-dashoffset: 0;
  }
}
@keyframes worm2 {
  from {
    stroke-dashoffset: 358;
  }
  50% {
    stroke-dashoffset: 0;
  }
  to {
    stroke-dashoffset: -358;
  }
}
</style>
<script>
import { defineComponent, computed } from "vue"
import { useStore } from "vuex"
import SpinLoader from "./SpinLoader"

export default defineComponent({
  name: "Loader",
  components: {
    SpinLoader
  },
  props: {
    logo: String
  },
  setup() {
    const store = useStore()

    const loaderType = computed(() => {
      return store.getters["config/layoutConfig"]("loader.type")
    })

    return {
      loaderType
    }
  }
})
</script>
