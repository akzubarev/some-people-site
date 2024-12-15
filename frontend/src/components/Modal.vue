<template>
  <!-- 	<teleport to="head">
      <meta name="theme-color" :content="gray800">
    </teleport> -->
  <teleport to="body">
    <div class="Popup-Overlay"></div>
    <div class="Popup" @click.self="$emit('close')">

      <div class="Popup-Content">
        <button class="absolute top-3 right-3 cursor-pointer"
                v-if="!hideX" @click="$emit('close')">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
               viewBox="0 0 24 24" fill="none">
            <path fill-rule="evenodd" clip-rule="evenodd"
                  d="M18.0304 7.02849L18.5608 6.49816L17.5001 5.4375L16.9698 5.96783L12.0001 10.9375L7.03045 5.96783L6.50012 5.4375L5.43946 6.49816L5.96979 7.02849L10.9395 11.9982L5.96978 16.9678L5.43945 17.4982L6.50011 18.5588L7.03044 18.0285L12.0001 13.0588L16.9698 18.0285L17.5001 18.5588L18.5608 17.4982L18.0304 16.9678L13.0608 11.9982L18.0304 7.02849Z"
                  fill="#DADFE6"/>
          </svg>
        </button>
        <div class="Popup-Body">
          <slot/>
        </div>
      </div>
    </div>
  </teleport>
</template>
<script setup>
// import resolveConfig from 'tailwindcss/resolveConfig'
// import tailwindConfig from '@/../tailwind.config.js'
// const gray800 = resolveConfig(tailwindConfig)['colors']['gray']['900']

defineEmits(['close'])
const props = defineProps(['hideX'])

</script>
<style lang="scss">
.Popup {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 200;
  height: 100%;
  width: 100%;
  // &-Close {
  // 	right: 18px;
  // 	top: 18px;
  // 	position: absolute;
  // 	z-index: 201;
  // }
  &-Content {
    background: theme('colors.gray.1000');
    width: 100%;
    position: relative;
    overflow-y: auto;
    max-height: 100%;
  }

  &-Overlay {
    position: fixed;
    left: 0;
    top: 0;
    height: 100%;
    width: 100%;
    overflow: hidden;
    z-index: 100;
    background: rgba(0, 0, 0, .7);
  }

  .card {
    background: theme('colors.gray.1000');
  }

  @media(min-width: 576px) {
    padding: 24px;
    &-Content {
      width: 500px;
      border-radius: 1rem;
    }
  }
}
</style>
