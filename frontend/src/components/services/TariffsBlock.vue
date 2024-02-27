<template>
  <ActionModal
      v-if="showTariffSwitchModal" type="info"
      @close="() => {showTariffSwitchModal = false}"
      @submit="() => {showTariffSwitchModal = false}"
      :title="$t('subscription.tariffSwitchTitle')"
      :buttonText="$t('common.actions.ok')">
  </ActionModal>
  <!--  <ActionModal-->
  <!--      v-if="showConfirmModal" type="info"-->
  <!--      @close="() => {showConfirmModal = false}"-->
  <!--      :title="$t('subscription.warningTitle')"-->
  <!--      :description="$t('subscription.warningDescription')"-->
  <!--      @submit="() => showBalance()"-->
  <!--      :buttonText="$t('common.actions.confirm')">-->
  <!--  </ActionModal>-->
  <ActionModal
      v-if="showBrokeModal" type="sad" button-style="solid"
      @close="() => {showBrokeModal = false}"
      :title="$t('subscription.noBalanceTitle')"
      :description="$t('subscription.noBalanceDescription')"
      @submit="() => $router.push('/wallet/pay-in')"
      :buttonText="$t('common.actions.topUp')">
    <template #icon>
      <inline-svg :src="require('@/assets/images/icons/Sad.svg')"/>
    </template>
  </ActionModal>

  <div class="flex flex-col gap-[48px]">
    <div class="mt-[48px] flex flex-col w-full items-center">
      <div
          class="flex justify-between w-full max-w-[670px] px-[24px] py-[16px]">
        <div>
          {{ $t("subscription.tariffTitle") }}
        </div>
        <div class="flex gap-[15px] md:!gap-12">
          <div class="min-w-[94px]">
            {{ $t("subscription.cost") }}
          </div>
        </div>
      </div>
      <div
          :class="['card flex flex-col justify-between w-full max-w-[670px] p-[24px] py-0', lighten&&'!bg-gray-800']">
        <div
            v-for="(plan, i) in subscriptionPlans" :key="i"
            :class="i < 2 && 'border-bottom !border-[--bs-body-color]'"
            @click="(selectedPlan=i)"
            class="flex justify-between w-full px-0 py-[16px] cursor-pointer gap-4"
        >
          <div class="text-white flex gap-[8px]">
            <div class="flex">
              <input
                  class="form-check-input !min-w-[1.5rem] !w-[1.5rem] !h-[1.5rem]"
                  type="radio" :checked="selectedPlan==i">
              <label class="form-check-label cursor-pointer">
                <span class="text-white">{{ plan.title }}</span>
                <span v-if="plan.discount" class="text-[--bs-body-color]"> -{{
                    plan.discount
                  }}%</span>
              </label>
            </div>
          </div>
          <div class="flex md:!gap-12 gap-[15px]">
            <span class="min-w-[94px]">
              <span class="text-white">{{ plan.price }}</span>
              <span class="text-[--bs-body-color]">/{{
                  String($t('common.periods.month')).toLowerCase()
                }}</span>
            </span>
          </div>
        </div>
        <div :class="['card cursor-pointer', $style.SpecialOffer]"
             @click="selectedPlan=3" v-if="specialOffer">
          <div class="card p-[12px] bg-[#13161A]">
            <div class="form-check">
              <input class="form-check-input !w-[1.5rem] !h-[1.5rem] mt-1 pe-2"
                     type="radio" :checked="selectedPlan==3">
              <div class="form-check-label">
                <div class="text-xl text-white">
                  {{ $t('subscription.specialoffer') }}
                </div>
                <div class="ps-8">
                  {{
                    $t('subscription.specialofferdesc_2', {
                      term: '3', date: '3.10', price: specialOffer
                    })
                  }}
                </div>
                <div class="flex pt-3 gap-3 ps-8">
                  <div class="min-w-[100px]">
                    <div class="text-4xl text-[var(--dark-accent-color)]">
                      {{ daysUntilDate() }}
                    </div>
                    {{ $t('subscription.daystoend') }}
                  </div>
                  <div class="min-w-[100px]">
                    <div class="text-4xl text-[var(--dark-accent-color)]">
                      {{ placesLeft }}
                    </div>
                    {{ $t('common.inStock') }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div>
      <div class="flex w-full justify-center">
        <button class="btn btn-accent mt-8 !px-[3rem]" v-show="selectedPlan==3"
                @click="subscribe">
          {{ $t('subscription.subscribe') }}
        </button>
        <button class="btn btn-accent mt-8 !px-[3rem]"
                v-show="selectedPlan!=3" @click="subscribe">
          {{ $t('subscription.subscribe') }} {{ prices[selectedPlan] }} USDT
        </button>
      </div>
      <div v-if="access" class="flex w-full justify-center">
        <div class="p-6">
          {{
            $t('subscription.subscribeduntill', {
              time: access === true && '01.01.2033' || moment(access).format('DD.MM.YYYY')
            })
          }}
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import {ref} from 'vue'
import {useStore} from 'vuex'
import ActionModal from '@/components/action-modal/ActionModal.vue'
import {useI18n} from 'vue-i18n'
import {useRouter} from 'vue-router'
import walletService from "@/services/walletService"
import moment from '@/utils/moment'

const store = useStore()
const {t} = useI18n()
const router = useRouter()
const props = defineProps({
  target: {default: "all", type: String},
  priceMonth: {default: 50, type: Number},
  priceHalfYear: {default: 250, type: Number},
  priceYear: {default: 450, type: Number},
  specialOffer: {default: 60, type: Number},
  period_ids: {default: () => [5, 4, 3, 2], type: Array},
  lighten: {default: false, type: Boolean}
})

const prices = []
const subscriptionPlans = []
const specialOfferIndex = ref(0)
const access = ref(props.target === "all" ?
    store.getters['auth/user'].access :
    store.getters['auth/user'].service_access[props.target] ||
    store.getters['auth/user'].access
)

if (props.priceMonth != null) {
  prices.push(props.priceMonth)
  subscriptionPlans.push({
    title: t('common.periods.month'),
    price: props.priceMonth
  })
}

if (props.priceHalfYear != null) {
  prices.push(props.priceHalfYear)
  subscriptionPlans.push({
    title: t('common.periods.halfYear'),
    price: parseInt(props.priceHalfYear / 6),
    discount: props.priceMonth ? parseInt(100 - props.priceHalfYear * 100 / (props.priceMonth * 6)) : null
  })
}

if (props.priceYear != null) {
  prices.push(props.priceYear)
  subscriptionPlans.push({
    title: t('common.periods.year'),
    price: parseInt(props.priceYear / 12),
    discount: props.priceMonth ?
        parseInt(100 - props.priceYear * 100 / (props.priceMonth * 12)) : props.priceHalfYear ?
            parseInt(100 - props.priceYear * 100 / (props.priceHalfYear * 2)) : null
  },)
}

if (props.specialOffer != null) {
  prices.push(props.specialOffer)
  specialOfferIndex.value = prices.length
}

const count = store.getters["subscription/get"].count
const placesLeft = count < 196 ? 196 - count : 0
// const showConfirmModal = ref(false)
const showBrokeModal = ref(false)
const showTariffSwitchModal = ref(false)
const selectedPlan = ref(specialOfferIndex.value)

// const showWarning = () => {
//   // showConfirmModal.value = true
// }
const showBalance = () => {
  // showConfirmModal.value = false
  walletService.wallet(1).then(({data}) => {
    if (data.balance >= prices[selectedPlan.value])
      router.push('/wallet/pay-in?period_id=' + props.period_ids[selectedPlan.value])
    else
      showBrokeModal.value = true
  })
}

const subscribe = () => {
  // ym(92969894, 'reachGoal', 'subscribe')
  // alert(t('subscription.inProgress'))
  // if (selectedPlan.value == 0) {
  //   selectedPlan.value = 3
  // showTariffSwitchModal.value = true
  // return
  // }
  // showWarning()
  showBalance()
}

const millisecondsPerDay = 24 * 60 * 60 * 1000;
const daysUntilDate = () => {
  const targetDate = new Date(
      Date.UTC(2023, 10 - 1, 3 - 1, 21, 0, 0)
  )
  return Math.ceil((targetDate - new Date()) / millisecondsPerDay);
}

</script>
<style module lang="scss">
.selected {
  background: linear-gradient(var(--accent-color-start), var(--accent-color-end)) !important;
  padding: 1px;
  margin: 0 calc(-1 * theme('spacing.3'));
  margin-bottom: theme('spacing.3');

}
</style>
