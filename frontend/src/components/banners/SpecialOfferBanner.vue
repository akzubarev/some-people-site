<template>
  <div class="flex flex-col gap-6 rounded-2xl p-6 so-banner-bg bg-cover"
       :style="`background-image: url('${require('@/assets/images/BannerBG-blue.png')}')`">
<!--    <div class="flex flex-wrap items-center">-->
<!--      <span-->
<!--          class="text-[&#45;&#45;dark-primary-color] border-[1px] border-[&#45;&#45;dark-primary-color] rounded-xl px-2">-->
<!--        {{ $t('subscription.specialoffer') }}-->
<!--      </span>-->
<!--    </div>-->
    <span class="text-4xl text-[--dark-text-color]">
      {{ $t('subscription.specialofferTitle') }}
    </span>
        <span class="text-[--dark-text-color]">
<!--          {{-->
<!--            $t('subscription.specialofferdesc_2', {-->
<!--              term: '3', price: 60-->
<!--            })-->
<!--          }}-->
          {{ $t('subscription.specialofferdesc') }}
        </span>
    <div class="flex gap-5 mt-3 flex-wrap">
      <button
          class="btn btn-outline w-full md:w-fit text-[--dark-text-color] !border-[--dark-text-color]"
          @click="$router.push('/subscription/instruments')">
        {{ $t('common.actions.open') }}
      </button>
<!--      <button-->
<!--          class="btn btn-outline w-full md:w-fit text-[&#45;&#45;dark-text-color] !border-[&#45;&#45;dark-text-color]"-->
<!--          @click="$router.push('/subscription/instruments')">-->
<!--        {{ $t('subscription.specialOfferVideo') }}-->
<!--      </button>-->
      <!--      <div clas="flex flex-col">-->
      <!--        <div class="text-[&#45;&#45;dark-primary-color]">-->
      <!--          {{ daysUntilDate() }} {{ $t('common.daysLeft') }}-->
      <!--        </div>-->
      <!--        <div class="text-[&#45;&#45;dark-primary-color]">-->
      <!--          {{ $t('common.timeLeft') }}-->
      <!--        </div>-->
      <!--      </div>-->
      <!--      <div class="flex flex-col">-->
      <!--        <div class="text-[&#45;&#45;dark-primary-color]">-->
      <!--          {{ placesLeft }}-->
      <!--        </div>-->
      <!--        <div class="text-[&#45;&#45;dark-primary-color]">-->
      <!--          {{ $t('common.inStock') }}-->
      <!--        </div>-->
      <!--      </div>-->
    </div>
  </div>
</template>

<style>
/* .so-banner-bg { */
/* } */
</style>

<script setup>
import Cookies from "js-cookie"
import {useStore} from "vuex"

const locale = 'en'
const timeLeft = 2000000
const store = useStore()
const count = store.getters["subscription/get"].count
const placesLeft = count < 196 ? 196 - count : 0

const formatTimer = secs => {
  const pad = (n) => n < 10 ? `0${n}` : n

  const h = Math.floor(secs / 3600)
  const m = Math.floor(secs / 60) - (h * 60)
  const s = Math.floor(secs - h * 3600 - m * 60)

  return `${pad(h)}:${pad(m)}:${pad(s)}`
}


const millisecondsPerDay = 24 * 60 * 60 * 1000;
// const currentPrice = () => {
//   const subDate = new Date(
//       Date.UTC(2023, 8 - 1, 20 - 1, 21, 0, 0)
//   )
//   return 300 + 10 * Math.floor((new Date() - subDate) / millisecondsPerDay)
// }

const daysUntilDate = () => {
  const targetDate = new Date(
      Date.UTC(2023, 10 - 1, 3 - 1, 21, 0, 0)
  )
  return Math.ceil((targetDate - new Date()) / millisecondsPerDay);
}

</script>
