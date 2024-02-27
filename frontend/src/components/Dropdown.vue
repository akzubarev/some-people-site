<template>
  <div class="Dropdown">
    <div class="Dropdown-Overflow" @click="isOpen=false" v-if="isOpen"/>
    <div @click="isOpen = !isOpen" class="Dropdown-Btn">
      <slot name="button"/>
    </div>

    <div ref="body" class="Dropdown-Body card"
      :class="[directionXClass, directionYClass]"
      v-if="isOpen">
      <div class="p-3">
        <slot/>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'


const isOpen = ref(false)
const props = defineProps(['directionX', 'directionY'])

const directions = {
  toRight: 'left-0',
  toLeft: 'right-0',
  toTop: 'bottom-0',
  toBottom: 'top-0',
}
const directionXClass = ref(directions[props.directionX])
const directionYClass = ref(directions[props.directionY])

const body = ref(null)

watch(isOpen, () => setTimeout(() => {
  const offsetX = 10 // px
  const offsetY = 10 // px

  if (body.value) {
    const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)
    const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
    const {right, left, top, bottom} = body.value.getBoundingClientRect()

    for (const [border, op] of Object.entries({
      right: { checker: o => right > vw - o, offset: offsetX, direction: 'directionX'},
      left: { checker: o => left < 0 + o, offset: offsetX, direction: 'directionX'},
      bottom: { checker: o => bottom > vh - o, offset: offsetY, direction: 'directionY'},
      top: { checker: o => top < 0 + o, offset: offsetY, direction: 'directionY'},
    })) {
    console.log(border, op.checker(op.offset), {right, left, top, bottom}[border], vw, vh)
      if (!props[op.direction] && op.checker(op.offset)) {
        body.value.style[border] = `${op.offset}px`
      }
    }
  }
}, 10))
</script>

<style lang="scss">
.Dropdown {
  position: relative;
  display: inline-block;
  &-Btn {
    @apply cursor-pointer;
  }

  /* Dropdown menu styles */
  &-Body {
    @apply absolute;
    z-index: 100;
  }
  &-Overflow {
    z-index: 99;
    position: fixed;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,.5);
    left: 0;
    top: 0;
  }
}

</style>
