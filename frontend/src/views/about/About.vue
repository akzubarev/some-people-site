<template>
   <div class="card">
    <div class="card-header border-0 ">
      <div class="card-title">
        {{ $t("menu.about") }}
      </div>
    </div>
  </div>
  <div class="gap-4 grid grid-cols-2 lg:grid-cols-4 gap-4 mb-5 mt-6">
    <div class="grid" v-for="stat in stats" :key="stat.title">
      <div class="card">
        <div class="card-header border-0 ">
          <div class="card-title">
            {{ stat.value || 0 }}
          </div>
        </div>
        <div class="card-body pt-0">
          <span>{{ stat.title }}</span>
        </div>
      </div>
    </div>
  </div>
  <div class="grid gap-4 grid-cols-1 lg:grid-cols-2 mb-3">
    <div class="card">
      <div
          class="card-header border-0 flex justify-between w-full"
          style="min-height: unset"
      >
        <div class="card-title">
          {{ $t("main.playersGeographyTitle") }}
        </div>
        <div class="flex items-center gap-2">
          <inline-svg
              class="text-2xl text-gray-400"
              :src="require('@/assets/images/icons/auth/eye.svg')"/>
          <div class="form-check form-switch m-0 p-0">
            <input
                type="checkbox"
                class="form-check-input m-0 min-w-[3rem]"
                v-model="globeShowRegistrations"
            />
          </div>
          <inline-svg
              class="text-2xl text-gray-400"
              :src="require('@/assets/images/icons/auth/person.svg')"/>
        </div>
      </div>

      <!-- <div id="globe" class="mb-5"></div> -->
      <!-- <SpinLoader/> -->
      <div class="card-body w-full pt-0">
        <!-- <Globe :target="globeShowRegistrations ? 'registrations' : 'visits'"/> -->
        <button
            @click="() => (showLocationRatingModal = true)"
            class="btn btn-outline w-full mt-3"
        >
          {{ $t("common.actions.showList") }}
        </button>
      </div>
      <LocationRatingModal
          :show="showLocationRatingModal"
          @close="() => (showLocationRatingModal = false)"
      />
    </div>

    <div class="grid">
      <div class="card">
        <div class="card-header !pb-0">
          <div class="card-title">
            {{ $t("main.lastRegistrationsTitle") }}

          </div>
        </div>
        <div class="card-body !pt-0 w-full h-full !pb-3">
          <div
              v-for="(user, i) in lastRegistrations"
              :key="`lr-${i}`"
              class="w-full flex flex-col"
          >
            <div class="flex w-full gap-4 py-3">
              <div class="flex">
                <avatar
                    size="35"
                    :country="user.country_iso || 'it'"
                    showFlag="true"
                    :src="user.avatar"
                    :username="user.first_name + ' ' + user.last_name"
                ></avatar>
              </div>
              <div class="flex w-full items-center">
                {{ user.email_hidden }}
              </div>
              <div class="flex items-center">
                {{
                  new Date(user.created_at).toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                    hour12: false
                  })
                }}
              </div>
            </div>
            <!--             <hr
                          class="my-3"
                          v-if="i !== lastRegistrations.length - 1"
                        /> -->
          </div>
        </div>
      </div>
    </div>

    <div class="card h-[488px] max-h-[488px] grid"
         style="grid-template-rows: auto 1fr">
      <div class="card-header !pb-3">
        <div class="card-title flex justify-between w-full">
          <span>
            {{ $t("main.countryRatingTitle") }}
          </span>
          <div class="flex items-center gap-2">
            <inline-svg
                class="text-2xl text-gray-400"
                :src="require('@/assets/images/icons/auth/person.svg')"/>
            <div class="form-check form-switch m-0 p-0">
              <input
                  type="checkbox"
                  class="form-check-input m-0 min-w-[3rem]"
                  v-model="countryRatingShowPercent"
              />
            </div>
            <inline-svg
                class="text-2xl text-gray-400"
                :src="require('@/assets/images/icons/auth/percent.svg')"/>
          </div>
        </div>
      </div>
      <div
          class="card-body overflow-auto !pt-0"
          style="scrollbar-color: #4f506c transparent"
      >
        <div
            v-for="(country, i) in countryRating.filter(c => c.iso)"
            :key="`cr-${i}`"
            class="w-full py-3"
        >
          <div class="flex w-full gap-4">
            <img
                class="rounded-full w-[35px] h-[35px]"
                style="object-fit: cover"
                :src="
                `https://flagcdn.com/h40/${country.iso.toLowerCase()}.png`
              "
            />

            <div class="flex w-full items-center">
              {{ country.name }}
            </div>
            <div class="flex items-center pe-2">
              {{
                countryRatingShowPercent
                    ? `${country.percent}%`
                    : country.sum.toLocaleString(undefined, {
                      minimumFractionDigits: 0
                    })
              }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="grid gap-6 grid-cols-1">
      <!--      bg-[#02122E]-->
      <div class="card relative">
        <img
            class="absolute" :src="require('@/assets/images/mg/tg.png')"
            style="right: 2em; height: 60%;top:20%;max-height: 100px;"
        />
        <div class="card-header border-0 ">
          <div class="card-title">
            {{ $t("main.telegramChannel") }}
          </div>
        </div>
        <div class="card-body pt-0 flex items-center"
             :class="$style.social_network">
          <a :href="$t('main.telegramChannelLink')"
             class="btn btn-outline btn-outline-primary">
            {{ $t("common.actions.go") }}
          </a>
        </div>
      </div>
      <div v-if="['ru','uk'].includes(lang)"
           class="card relative">
        <img class="absolute"
             :src="require('@/assets/images/mg/tg-chat.png')"
             style="right: 2em; height: 60%;top:20%;max-height: 100px;"
        />
        <div class="card-header border-0 ">
          <div class="card-title">
            {{ $t("main.telegramChat") }}
          </div>
        </div>
        <div class="card-body pt-0 flex items-center"
             :class="$style.social_network">
          <a :href="$t('main.telegramChatLink')"
             class="btn btn-outline btn-outline-primary">
            {{ $t("common.actions.go") }}
          </a>
        </div>
      </div>
      <!--      bg-[#130F2C]-->
      <div class="card relative">
        <img class="absolute"
             :src="require('@/assets/images/mg/tg-aircraft.png')"
             style="right: 2em; height: 70%; top:15%;max-height: 100px;"
        />
        <div class="card-header border-0 ">
          <div class="card-title flex w-full">
            {{ $t("main.telegramBot") }}
          </div>
        </div>
        <div class="card-body pt-0 flex items-center w-full"
             :class="$style.social_network">
          <button @click="$router.push('/account/telegram')"
                  class="btn btn-outline btn-outline-info">
            {{ $t("common.actions.connect") }}
          </button>
        </div>
      </div>
      <!--      bg-[#1a0a22]-->
      <div class="card relative">
        <img class="absolute"
             :src="require('@/assets/images/mg/ig.png')"
             style="right: 2em; height: 60%;top:20%;max-height: 100px;"
        />
        <div class="card-header border-0 ">
          <div class="card-title">
            {{ $t("main.instagram") }}
          </div>
        </div>
        <div :class="$style.social_network"
             class="card-body pt-0 flex items-center">
          <a :href="$t('main.instagramLink')"
             class="btn btn-outline btn-outline-danger">
            {{ $t("common.actions.go") }}
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {defineComponent, ref, watch} from "vue"
import {defineAsyncComponent} from "vue"
import {useI18n} from "vue-i18n"
import {useStore} from "vuex"
import Avatar from "@/components/avatar"
import LocationRatingModal from "@/views/about/LocationRatingModal.vue"
import walletService from "@/services/walletService"
import authService from "@/services/authService"
import SpinLoader from "@/components/SpinLoader.vue"


export default defineComponent({
  name: "dashboard",
  components: {
    Avatar,
    Globe,
    LocationRatingModal,
  },
  setup() {
    const t = useI18n().t
    const dashboard = ref({})
    const store = useStore()
    const stats = ref([
      {
        title: t("main.stats.countRegistered")
      },
      {
        title: t("main.stats.countActive")
      },
      {
        title: t("main.stats.countCountries")
      },
      {
        title: t("main.stats.totalEarned")
      }
    ])

    const showAllCountryRating = ref(false)
    const countryRatingShowPercent = ref(true)
    const globeShowRegistrations = ref(false)
    const showLocationRatingModal = ref(false)
    const lastRegistrations = ref([])
    const countryRating = ref([])
    const lang = store.getters['auth/user'].locale || "en"

    const getCountryRating = async top =>
        (countryRating.value = (await authService.countryRating(top)).data)

    const getWalletStats = async () => {
      await walletService.totalEarned().then(({data}) => {
        stats.value[3].value = `${data.total_income.toLocaleString(undefined, {
          minimumFractionDigits: 0
        })} USDT`
      })
    }
    const getLastRegistrations = async () => {
      dashboard.value.lastRegistrations = (
          await authService.lastRegistrations()
      ).data
      lastRegistrations.value = dashboard.value.lastRegistrations
    }
    const getUsersStats = async () => {
      dashboard.value.usersStats = (await authService.stats()).data
      stats.value[0].value = `${dashboard.value.usersStats.count_registered.toLocaleString(
          undefined,
          {minimumFractionDigits: 0}
      )}`
      stats.value[1].value = `${dashboard.value.usersStats.count_active.toLocaleString(
          undefined,
          {minimumFractionDigits: 0}
      )}`

      stats.value[2].value = `${dashboard.value.usersStats.count_countries}`
    }
    const buildStats = () => {
      // await getBalance()

      getCountryRating(/*countryRatingTopCount*/)
      getWalletStats()
      getLastRegistrations()
      getUsersStats()

      // stats.value[2] = {
      //   title: t("main.stats.countStudents"),
      //   value: `${dashboard.value.usersStats.count_students.toLocaleString(undefined, {minimumFractionDigits: 0})}`,
      // }

      // stats.value[3].value = `${dashboard.value.userBalance.balance} RSN`
    }

    buildStats()
    watch([() => showLocationRatingModal.value], () => {
      if (showLocationRatingModal.value) {
        document.body.classList.add("overflow-hidden", "position-fixed")
        // window.HelpCrunch("hideChatWidget")
      } else {
        document.body.classList.remove("overflow-hidden", "position-fixed")
        // window.HelpCrunch("showChatWidget")
      }
    })

    return {
      stats,
      lastRegistrations,
      countryRating,
      showAllCountryRating,
      countryRatingShowPercent,
      getCountryRating,
      globeShowRegistrations,
      showLocationRatingModal,
      lang
    }
  }
})
</script>


<style module lang="scss">
.social_network {
  @apply bg-transparent #{!important};
}
</style>
