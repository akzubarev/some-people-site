<template>
  <div class="flex flex-col" :class="checklistExpanded ? 'gap-3' : ''">
    <div
        @click="checklistExpanded = !checklistExpanded; $emit('expand', checklistExpanded)"
        class="flex flex-col items-center gap-1 pe-2 cursor-pointer card-header"
    >
      <div class="flex flex-row w-full items-center justify-between">
        <div class="card-title">{{ $t('main.checklist.title') }}</div>
        <inline-svg
            :class="[s.arrow, { [s.arrow_expanded]: checklistExpanded }]"
            :src="require('@/assets/images/icons/chevrone.svg')"
        />
      </div>
      <div class="flex flex-col w-full gap-1">
        <ProgressBar
            class="!h-[4px]" :progress="(completed / total) * 100"
        />
        <span>{{
            $t('main.checklist.completedOf', {completed, total})
          }}</span>
      </div>
    </div>
    <div
        class="flex flex-col justify-center transition-all overflow-hidden duration-300 pt-0 gap-6"
        :class="checklistExpanded ? 'card-body h-wrap' : 'h-0'"
    >
      <div class="flex flex-col gap-5">
        <div v-for="a in achievements" :key="a"
             class="flex items-center gap-4">
          <div class="form-check m-0 p-0">
            <input type="checkbox"
                   class="form-check-input m-0 checked:!bg-[--dark-accent-color] checked:!border-[--dark-accent-color] disabled:!opacity-100"
                   @input="() => {a.done = !a.done; handleCheck(a.query)}"
                   :checked="a.done" :disabled="a.readonly"/>
          </div>
          <div class="flex items-center w-full gap-4" role="button"
               @click="a.callback">
          <span class="w-full" :class="a.done ? 'text-muted' : 'text-white'">{{
              a.title
            }}</span>
            <inline-svg
                class="text-[0.7rem] w-[16px] h-[16px] text-[var(--dark-text-color)] -rotate-90"
                :src="require('@/assets/images/icons/chevrone.svg')"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue"
import {useRouter} from "vue-router"
import {useI18n} from "vue-i18n"
import {useStore} from "vuex"
import ProgressBar from "@/components/progressbar"
import achievesService from "@/services/achievesService"
import s from "@/components/filters/styles.module.scss";


const {t} = useI18n()
const router = useRouter()
const store = useStore()
defineEmits(["expand"])
const user = store.getters["auth/user"]
const checklistExpanded = ref(false)

const achievements = ref([
  {
    title: t('main.checklist.telegramBot'),
    callback: () => router.push('/account/telegram'),
    query: 'TelegramConnectedAchieve',
    done: !!user.telegram,
    readonly: true,
  },
  {
    title: t('main.checklist.activities'),
    callback: () => window.open(t('main.residualActivitiesLink'), "_blank"),
    query: 'ActivitiesChatJoinedAchieve',
  },
  {
    title: t('main.checklist.telegramChannel'),
    callback: () => window.open(t('main.telegramChannelLink'), "_blank"),
    query: 'TelegramChannelJoinedAchieve',
  },
  // TelegramChatJoinedAchieve added dynamically
  {
    title: t('main.checklist.instagram'),
    callback: () => window.open(t('main.instagramLink'), "_blank"),
    query: 'InstagramSubscribedAchieve',
  },
  // {
  //   title: t('main.checklist.youtube'),
  //   callback: () => window.open(t('main.youtubeLink', "_blank")),
  //   query: '',
  // },
  {
    title: t('main.checklist.communityPresentation'),
    callback: () => window.open('https://residual.community' + t('promo.sharePresentation.url'), "_blank"),
    query: 'CheckCommunityPromoAchieve',
  },
  {
    title: t('main.checklist.marketingPresentation'),
    callback: () => window.open('https://residual.community/docs/marketing-en.pdf', "_blank"),
    query: 'CheckMarketingPromoAchieve',
  },
  {
    title: t('main.checklist.purchaseTariff'),
    callback: () => router.push('/tariffs'),
    query: 'MatrixCompletedAchieve',
    readonly: true,
  },
])

const lang = store.getters['auth/user'].locale || "en"
if (['ru', 'uk'].includes(lang))
  achievements.value.splice(3, 0,
      {
        title: t('main.checklist.telegramChat'),
        callback: () => window.open(t('main.telegramChatLink'), "_blank"),
        query: 'TelegramChatJoinedAchieve',
      }
  )
const completed = ref(0)
const total = achievements.value.length

const updateList = async () => {
  const data = (await achievesService.list()).data
  for (const achieve of data) {
    const idx = achievements.value.findIndex(v => v.query == achieve.key)
    if (idx != -1) {
      achievements.value[idx].done = true
      achievements.value[idx].readonly = true
    }
  }
  completed.value = achievements.value.filter(v => v.done).length
}
updateList()

const handleCheck = async (query) => {
  completed.value = achievements.value.filter(v => v.done).length
  await achievesService.createAchieve({key: query})
}
</script>
