<template>
  <carousel
    :breakpoints="{
      0: {
        itemsToShow: 1.2
      },
      920: {
        itemsToShow: 1.0
      }
    }"
    :wrap-around="true"
    class="h-full"
  >
    <slide v-for="(item, i) in items" :key="i">
      <div class="grid h-full w-full mx-2 lg:mx-0 mx-lg-0">
        <div class="card">
          <div class="card-header border-0 ">
            <div class="card-title text-uppercase">
              {{ item.title }}
            </div>
          </div>
          <div class="card-body text-start pt-0 text-block">
            <div
              v-if="item.tags && item.tags.length"
              class="flex gap-2 flex-wrap pb-5"
            >
              <div
                v-for="(tag, i) in item.tags"
                :key="'tag-' + i"
                class="px-2 border border-1 rounded-xl"
                :style="
                  `border-color: ${tag.color} !important; color: ${tag.color}`
                "
              >
                <span>
                  {{ tag.title }}
                </span>
              </div>
            </div>
            {{ item.description }}
          </div>
        </div>
      </div>
    </slide>

    <template #addons>
      <pagination />
    </template>
  </carousel>
</template>

<style lang="scss">
.text-block {
  white-space: pre-line;
}
</style>

<script>
import "vue3-carousel/dist/carousel.css"
import { defineComponent, onMounted } from "vue"
import { Carousel, Slide, Pagination } from "vue3-carousel"
export default defineComponent({
  name: "base-carousel",
  props: ["items", "id"],
  components: {
    Carousel,
    Slide,
    Pagination
  },
  setup() {
    // left: 37, up: 38, right: 39, down: 40,
    // spacebar: 32, pageup: 33, pagedown: 34, end: 35, home: 36
    const keys = { 37: 1, 38: 1, 39: 1, 40: 1 }

    function preventDefault(e) {
      e.preventDefault()
    }

    function preventDefaultForScrollKeys(e) {
      if (keys[e.keyCode]) {
        preventDefault(e)
        return false
      }
    }

    // modern Chrome requires { passive: false } when adding event
    let supportsPassive = false
    try {
      window.addEventListener(
        "test",
        null,
        Object.defineProperty({}, "passive", {
          get: function() {
            supportsPassive = true
            return ""
          }
        })
      )
    } catch (e) {
      console.log(e)
    }

    const wheelOpt = supportsPassive ? { passive: false } : false
    const wheelEvent =
      "onwheel" in document.createElement("div") ? "wheel" : "mousewheel"

    // call this to Disable
    function disableScroll() {
      window.addEventListener("DOMMouseScroll", preventDefault, false) // older FF
      window.addEventListener(wheelEvent, preventDefault, wheelOpt) // modern desktop
      window.addEventListener("touchmove", preventDefault, wheelOpt) // mobile
      window.addEventListener("keydown", preventDefaultForScrollKeys, false)
    }

    // call this to Enable
    function enableScroll() {
      window.removeEventListener("DOMMouseScroll", preventDefault, false)
      window.removeEventListener(wheelEvent, preventDefault, wheelOpt)
      window.removeEventListener("touchmove", preventDefault, wheelOpt)
      window.removeEventListener("keydown", preventDefaultForScrollKeys, false)
    }
    onMounted(() => {
      [...document.getElementsByClassName("carousel__track")].forEach(e => {
        e.addEventListener("mousedown", disableScroll)
        e.addEventListener("touchstart", disableScroll)
        e.addEventListener("mouseup", enableScroll)
        e.addEventListener("touchend", enableScroll)
      })

      /* for (const i in props.items) {
	  const item = document.querySelector(`#cr-ds-item-${props.id}-${i}`)
	  let targetHeight
	  targetHeight = item.clientHeight
	  if (window.getComputedStyle(item).display == "none") {
	  item.style.display = "block"
	  targetHeight = item.clientHeight
	  item.style.display = "none"
	  }
	  if ( props.mh.value < targetHeight) props.mh.value = targetHeight
	* } */
    })

    return {}
  }
})
</script>
