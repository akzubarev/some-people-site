<template>
  <div class="flex flex-row gap-1 rounded-2xl bg-cover"
       :style="`background-image: url('${image}')`">
    <div class="flex flex-col gap-5 p-5 bg-black bg-opacity-70"
         :class="full? 'w-[50%]' : 'w-[40%]'">
      <div class="text-4xl font-bold">
        {{ title }}
      </div>
      <div class="whitespace-pre-wrap">
        {{ description }}
      </div>
      <div class="flex gap-2" :class="full ? 'flex-row' : 'flex-col'">
        <div v-for="data in tags" :key="data"
             class="px-2 border w-fit h-fit border-1 rounded-xl text-md text-gray-500 border-gray-500">
          {{ data }}
        </div>
      </div>
      <div class="flex flex-col gap-5 flex-wrap">
        <a v-for="button in buttons" :key="button" :href="button.href"
           class="btn btn-outline w-full md:w-fit
          hover:text-content-accent hover:bg-[#0f6099] !border-[--text-color]">
          {{ button.text }}
        </a>
        <div class="flex flex-row gap-3 flex-wrap"
             v-if="Object.values(social).filter(link => !!link).length > 0">
          <inline-svg
              v-for="key in Object.keys(social).filter((k) => !!social[k])"
              :key="key"
              class="!w-8 !h-8 text-2xl text-gray-400 cursor-pointer"
              @click="goToSocial(social[key])" :src="social_icons[key]"
          />
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import {useStore} from "vuex"
import {useI18n} from "vue-i18n";

const store = useStore()
const {t} = useI18n()

const props = defineProps(["image", "title", "description", "tags", "buttons", "full", "social"])


const millisecondsPerMinute = 60 * 1000;
const millisecondsPerHour = 60 * millisecondsPerMinute;
const millisecondsPerDay = 24 * millisecondsPerHour;

const targetDate = new Date(
    Date.UTC(2023, 10 - 1, 29, 18, 0, 0)
)
const timeUntilDate = () => {
  const now = new Date()
  const days = Math.floor((targetDate - now) / millisecondsPerDay);
  const hours = Math.floor(((targetDate - now) % millisecondsPerDay) / millisecondsPerHour)
  const minutes = Math.max(0, Math.floor(((targetDate - now) % millisecondsPerHour) / millisecondsPerMinute))
  const days_str = days > 0 ? `${days} дней` : ''
  const hours_str = hours > 0 ? `${hours} часов` : ''
  const minutes_str = `${minutes} минут`
  return days_str + hours_str + minutes_str
}

const social_icons = {
  "vk": require('@/assets/images/icons/social/vk.svg'),
  "tg": require('@/assets/images/icons/social/tg.svg'),
  "ig": require('@/assets/images/icons/social/ig.svg')
}
const goToSocial = (link) => {
  window.open(link, '_blank').focus()
}
</script>
