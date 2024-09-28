<template>
  <!--begin::details View-->
  <div class="card mb-5 mb-xl-10 mt-6">
    <div v-if="settingsMatrix.length > 0" class="card-body flex flex-wrap gap-6 justify-between">
      <template v-for="group, j in targetGroups" :key="group.key">
        <div class="grid grid-cols-[auto_min-content] gap-3 w-full lg:flex-1 h-fit">

          <div class="flex text-xl pb-3">{{ group.title }}</div>
          <div class=""></div>

          <template v-for="row, i in settings" :key="i">
            <div class="">
              {{ row.title }}
            </div>
            <div class="grid justify-end items-center form-check m-0 p-0">
              <input type="checkbox" class="form-check-input m-0"
                @input="() => settingsMatrix[i][j] = !settingsMatrix[i][j]" :checked="settingsMatrix[i][j]" />
            </div>
          </template>
          <template v-if="group.key == 'team'">
            <div class="flex items-center">{{ $t('matrix.tree.depth') }}</div>
            <Dropdown direction-y='toTop'>
              <template #button>
                <div
                  class="btn rounded-2 bg-secondary !px-1 !py-0 flex gap-2 justify-between items-center whitespace-nowrap w-fit text-[15px]"
                  role="button">
                  {{ teamDepthEnum[teamDepth].title }}
                  <inline-svg
                    width="9px"
                    :src="require('@/assets/images/icons/matrix/Down.svg')"
                  />
                </div>
              </template>
                <ul class="w-full overflow-y-auto">
                  <li
                    v-for="item, i in teamDepthEnum"
                    :key="i"
                    class="nav-item w-full py-2"
                  >
                    <div
                      @click="() => teamDepth = i"
                      role="button"
                      class="nav-link text-active-primary me-6 whitespace-nowrap"
                      active-class="active"
                      :class="[i == teamDepth && 'active']"
                    >
                      {{ item.title }}
                    </div>
                  </li>
                </ul>
            </Dropdown>
          </template>
        </div>
        <div class="lg:pr-[4rem]" v-if="j + 1 < targetGroups.length"/>
      </template>
      <div class="flex justify-end w-full border-top pt-5">
        <button class="btn btn-primary h-fit w-full md:w-fit" @click="save">
          {{ $t(`common.actions.save`) }}
        </button>
      </div>
    </div>
  </div>
  <!--end::Row-->
</template>

<script setup>
import { onMounted, ref } from "vue"
import notificationService from "@/services/notificationService"
import { useI18n } from 'vue-i18n'
import Dropdown from '@/components/Dropdown.vue'


const t = useI18n().t;
const settingsMatrix = ref([])
const settingsData = ref({})
const teamDepthEnum = [
  {title: t('matrix.progress.allReferals')},
  {title: t('matrix.progress.referals')},
  {title: `2 Line`},
  {title: `3 Line`},
  {title: `4 Line`},
  {title: `5 Line`},
  {title: `6 Line`},
  {title: `7 Line`},
  {title: `8 Line`},
  {title: `9 Line`},
  {title: `10 Line`},
  {title: `11 Line`},
  {title: `12 Line`},
  {title: `13 Line`},
  {title: `14 Line`},
  {title: `15 Line`},
]
const teamDepth = ref(1)
const settings = [
  { title: t('settings.notifications.withdrawal'), types: ["WithdrawNotification"] },
  { title: t('settings.notifications.purchases'), types: ["ActivateMatrixNotification", "SubscriptionNotification", "ResubscriptionNotification"] },
  // { title: t('matrix.tree.newClone'), types: ["NewCloneNotification"] },
  // { title: t('settings.notifications.achievements'), types: ["MatrixCompletedNotification"] },
  { title: t('settings.notifications.rank'), types: ["RankNotification"] },
  { title: t('settings.notifications.bonuses'), types: ["MatrixBonusNotification", "ReferalBonusNotification"] },
  { title: t('settings.notifications.arena'), types: ["ArenaNotification"] },
]
const targetGroups = [
  { key: "personal", title: t('common.personal') },
  { key: "team", title: t('common.team') },
]

const loadSettings = async () => {
  const data = (await notificationService.telegram()).data.settings
  for (const i in targetGroups) {
    for (const j in settings) {
      if (!settingsMatrix.value[j]) {
        settingsMatrix.value[j] = []
      }
      settingsMatrix.value[j][i] = settings[j].types.reduce((a, v) => a && !!data[targetGroups[i].key][v], true)
    }
  }
  if (data.team.depth)
    teamDepth.value = data.team.depth
  settingsData.value = data
}

loadSettings()

const save = async () => {
  settingsMatrix.value.forEach((n, i) => {
    const types = settings[i].types
    types.forEach(t => {
      targetGroups.forEach((g, i) => settingsData.value[g.key][t] = n[i])
    })
  })
  settingsData.value.team.depth = teamDepth.value
  await notificationService.saveSettings(settingsData.value)
  /* @ts-ignore */
  // Swal.fire({
  //   icon: "success",
  // })
}
</script>
