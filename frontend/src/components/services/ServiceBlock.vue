<template>
  <div :class="['card', $style.card]" :style="style">
    <div :class="[fluid&&'grid-cols-1 lg:grid-cols-2', 'grid h-full']"
         :style="{background: `${services[service].color}9F`}">
      <div :class="[reverse&&'order-2', 'p-6']">
				<span class="border rounded-full border-gray-900 px-2 text-sm">
					{{ tag }}
				</span>
        <div class="text-3xl mt-2">
          {{ services[service].title }}
        </div>
        <template v-if="!noAction">
          <button
              @click="toService"
              class="border rounded-xl border-gray-900 px-3 py-2 text-sm mt-2"
              v-if="['vizi','avatar','gpt','bot'].includes(service)"
          >
            {{ $t('subscription.serviceblock.open') }}
          </button>
        </template>
      </div>
      <img
          :src="require(`@/assets/images/subscription_services/${service}.png`)"
          class="self-end">
    </div>

  </div>
  <Popup v-if="showPopup" @close="showPopup=false">
    <SmallSubscription/>
  </Popup>
</template>
<script setup>
import Popup from '@/components/Popup.vue'
import SmallSubscription from '../../views/subscription/SmallSubscription.vue'
import {ref} from 'vue'
import services from './services'


import store from '@/store'
import router from '@/router'

const showPopup = ref(false)
const showPage = ref(false)
const props = defineProps({
  // color: String,
  fluid: Boolean,
  // title: String,
  // image: String,
  service: String,
  tag: String,
  reverse: Boolean,
  style: String,
  noAction: Boolean
})

const access = store.getters['auth/user'].access
// const route = () => {
//   if (access) {
//     if (props.destination === "vizi")
//       showPage.value = true
//   } else
//     showPopup.value = true
// }
const toService = () => {
  if (props.service === "gpt")
    return window.open(`https://t.me/ResidualGPTbot`, '_blank').focus()
  if (props.service === "avatar")
    return window.open(`https://t.me/ResidualAIbot`, '_blank').focus()
  router.push(`/subscription/services/${props.service}`)
}
const successPopup = text => {
  setTimeout(() => {
    // Swal.fire({
    //   icon: "success",
    //   text: text
    // })
  }, 20)
}

const errorPopup = text => {
  setTimeout(() => {
    Swal.fire({
      icon: "error",
      text: text
    })
  }, 20)
}

</script>
<style lang="scss" module>
.card {
  @apply overflow-hidden text-gray-900;
  background: url('@/assets/images/subscription_services/pattern.jpg');
  background-size: cover;
  // background: #DAC3E5 url('@/assets/images/subscription_services/pattern.png');
}

</style>
