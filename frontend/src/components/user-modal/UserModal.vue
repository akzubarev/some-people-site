<template>
  <Popup v-if="user && Object.keys(user).length > 0" @close="$emit('close')">
    <div class="flex flex-col gap-[20px] p-3">
      <div class="flex p-0 pt-4 gap-4">
        <Avatar
            :src="user.avatar"
            :avatar-class="$style.avatar"
            :username="`${user.first_name || '-'} ${user.last_name || '-'}`"
            :country="user.country_iso || 'it'"
            showFlag="true"
            size="55"
        />
        <div class="flex flex-col gap-1">
          <div class="flex gap-2">
            <div>
              <div class="flex gap-1 items-center">
                <h5 class="flex gap-1 mb-1">
                  {{ user.first_name }}
                  {{ user.last_name }}
                  <span class="text-muted fw-normal">{{
                      user.referals_count || user.linear_referals_count
                    }}</span>

                  <div
                      v-if="user.matrix_uuid"
                      role="button"
                      @click="$emit('loadMatrix')"
                      class="p-0 w-fit flex items-center text-[0.5rem] -rotate-90"
                  >
                    <inline-svg
                        class="w-[16px] h-[16px]"
                        :src="require('@/assets/images/icons/chevrone.svg')"
                    />
                  </div>
                </h5>
                <img v-if="user.access"
                     class="rounded-full h-[16px] w-[16px] mb-2"
                     :src="require('@/assets/images/icons/subbed.svg')"
                />
              </div>
              <span
                  v-if="user.matrix_uuid && !showUserNameInTitle"
                  class="text-muted"
              >
                {{ user.matrix_uuid.split("-")[0] }}
              </span>
              <span v-else class="text-muted">
                {{ user.username }}
              </span>
            </div>
          </div>
        </div>
      </div>
      <slot>
        <div :class="$style.modal_block" v-if="userDisplayedStats.length">
          <div
              v-for="stat in userDisplayedStats"
              :key="stat.key + user.uuid"
              class="flex justify-between"
          >
            <span class="text-light">{{ stat.title }}</span>
            <div
                :class="$style.link"
                v-if="stat.formatter"
                v-html="stat.formatter(user[stat.key])"
            />
            <span v-else class="text-light">{{ user[stat.key] }}</span>
          </div>
        </div>
        <div :class="$style.modal_block">
          <div class="flex justify-between">
            <span>{{ $t("common.country") }}</span>
            <div class="flex items-center gap-2">
              <img
                  class="rounded-full h-[20px] w-[20px]"
                  :src="
                  `https://flagcdn.com/h20/${(
                    user.country_iso || 'HU'
                  ).toLowerCase()}.png`
                "
              />
              <span>{{ user.country }}</span>
            </div>
          </div>
          <div v-if="variant === 'team'" class="flex justify-between">
            <span>{{ $t("common.timezone") }}</span>
            <span>{{ user.timezone || "UTC+3" }}</span>
          </div>
          <div class="flex justify-between">
            <!--            {{ user.locale }}-->
            <span>{{ $t("settings.registrationDate") }}</span>
            <span> {{ getRegistrationDate(user.created_at) }} </span>
          </div>
          <div class="flex justify-between">
            <span class="text-light">{{ $t("user.referer") }}</span>
            <span class="text-light">{{
                user.refer_username
              }}</span>
          </div>
        </div>
        <div v-if="!isCurators" :class="$style.modal_block">
          <TariffsFilter
              :modal="true" :readonly="true"
              :targetTariffs="user.tariffs.map((tarrif_num) =>{
                     return  {0:0, 10:1, 20:2, 30:3, 40:4, 50:5}[tarrif_num]
                 })">
            {{ $t("common.tariff") }}: {{ user.tariff.title }}
          </TariffsFilter>
        </div>
        <div v-if="isTeam" :class="$style.modal_block">
          <div class="flex justify-between">
            <span>{{ $t("common.rank") }} #{{
                qualification.num / 10
              }}</span>
            <span>{{
                (qualification.depth_percent * 100).toLocaleString(
                    undefined, {maximumFractionDigits: 2}
                )
              }}%
            </span>
          </div>
          <div class="flex justify-between">
            <div v-if="tasks" class="flex flex-col gap-3 w-full">
              <span>{{ $t("common.nextRank") }} #{{
                  qualification.num / 10 + 1
                }}</span>
              <div class="card bg-gray-800 flex flex-col gap-3 p-6"
                   v-for="(task, index) in tasks" :key="index">
                <div class="text-xl">
                  {{ {"Turnover": $t("common.turnover")}[task.data.title] }}
                </div>
                <ProgressBar
                    :progress="(task?.progress[0] || 0)/(task?.progress[1] || 100)*100"
                />
                <div class="flex justify-between">
                  <span>
                    {{ task.progress[0] }}
                    <span class="text-gray-400">USDT</span>
                  </span>
                  <span>
                    {{ task.progress[1] }}
                    <span class="text-gray-400">USDT</span>
                  </span>
                </div>
              </div>
            </div>
          </div>
<!--          <div class="flex justify-between">-->
<!--            <span>{{ $t('user.profile.firstLineTurnover') }}</span>-->
<!--            <span>-->
<!--              {{ turnover1L }}-->
<!--              <span class="text-gray-400">USDT</span>-->
<!--            </span>-->
<!--          </div>-->
        </div>

        <div v-if="isTeam" :class="$style.modal_block">
          <div v-for="stat in userStats" :key="stat"
               class="flex justify-between">
            <span>{{ stat.title }}</span>
            <span>{{ stat.value }}
                <span v-if="stat.postfix" class="text-gray-400">
                  {{ stat.postfix }}
                </span>
            </span>
          </div>
        </div>
      </slot>
    </div>
  </Popup>
</template>

<script setup>
import {computed, ref, watch} from "vue"
import Avatar from "@/components/avatar/Avatar.vue"
import Popup from "@/components/Popup"
import {useI18n} from "vue-i18n"
import {useStore} from "vuex";
import TariffsFilter from "@/components/filters/TariffsFilter.vue";
import ProgressBar from "@/components/progressbar";
import achievesService from "@/services/achievesService";
import walletService from "@/services/walletService";
import authService from "@/services/authService";

const store = useStore()
const locale = store.getters['auth/user'].locale || 'en'
const {t} = useI18n()
const show = true
const props = defineProps({
  user: {}, variant: String // 'arena' | 'team' | 'rating'
})
const emits = defineEmits(["close", "loadMatrix"])
const userNameStat = {
  key: "username",
  title: t("user.username")
}

const getRegistrationDate = date => {
  return new Date(date)
      .toLocaleString(locale, {
        year: "numeric", month: "long", day: "numeric", hour12: false
        // hour: 'numeric', minute: 'numeric',
      })
}

const isRating = props.variant === "rating"
// const isArena = props.variant === "arena"
const isCurators = props.variant === "curators"
const isTeam = props.variant === "team"
const showUserNameInTitle = isRating || isTeam

const displayedStats = [
  !showUserNameInTitle && userNameStat,
  {
    key: "phone",
    title: t("user.phone"),
    formatter: value => `<a href="tel:${value}">${value}</a>`
  },
  {
    key: "telegram",
    title: t("user.telegram"),
    formatter: value => `<a href="https://t.me/${value}">@${value}</a>`
  },
  {
    key: "instagram",
    title: t("user.instagram"),
    formatter: value =>
        `<a href="https://www.instagram.com/${value}">@${value}</a>`
  },
  {
    key: "email",
    title: t("user.email"),
    formatter: value => `<a href="mailto:${value}">${value}</a>`
  }
].filter(Boolean)

const userDisplayedStats = computed(() => {
  return displayedStats.filter(
      s => Object.keys(props.user).includes(s.key) && props.user[s.key]
  )
})

const segments = ref([])
const referals = ref(0)
const payed_partners = ref(0)
const payout_sum = ref(0)
const income = ref(0)
const turnoverMonth = ref(0)
const turnoverAll = ref(0)
const turnover1L = ref(0)
const qualification = ref(0)

const tasks = computed(() => {
  const segment = segments.value ? segments.value['Status' + (qualification.value.num + 10)] : null
  return !!segment ? segment.tasks : null
})

if (isTeam) {
  achievesService.segment('P2PSegment', props.user.uuid).then(({data}) => {
    segments.value = data.segments
  })
  walletService.structureTurnover(props.user.uuid).then(({data}) => {
    turnoverMonth.value = data.month || 0
    turnoverAll.value = data.total || 0
  })

  walletService.firstLineTurnover(props.user.uuid).then(({data}) => {
    turnover1L.value = data.month || 0
  })

  authService.user_stats(props.user.uuid).then(({data}) => {
    qualification.value = data.qualification || {}
    referals.value = data.referals || 0
    payed_partners.value = data.payed_partners || 0
    payout_sum.value = data.payout_sum || 0
    income.value = data.earned || 0 //.toLocaleString(undefined, {
    //   maximumFractionDigits: 0
    // })
  })
}

const userStats = computed(() => [
  {title: t('user.profile.registered'), value: referals},
  {title: t('user.profile.payedPartners'), value: payed_partners},
  {title: t('user.profile.payouts'), value: payout_sum, postfix: 'USDT'},
  {title: t('user.profile.referals'), value: referals},
  {
    title: t('user.profile.turnoverMonth'),
    value: turnoverMonth, postfix: 'USDT',
  },
  {
    title: t('user.profile.turnoverAll'),
    value: turnoverAll, postfix: 'USDT',
  },
  {
    title: t('user.profile.firstLineTurnover'),
    value: turnover1L, postfix: 'USDT',
  },
  {title: t('user.profile.income'), value: income, postfix: 'USDT'},
])
</script>

<style module lang="scss">
.modal_block {
  @apply bg-[#15171A] rounded-xl flex flex-col gap-[20px] p-4;
}

.link {
  // @apply text-[var(--dark-link-color)];
  @apply text-blue-500;
  a {
    // @apply text-[var(--dark-link-color)];
    @apply text-blue-500;
    &:hover {
      opacity: 0.85;
    }
  }
}

.avatar {
  width: 48px;
  height: 48px;
}
</style>
