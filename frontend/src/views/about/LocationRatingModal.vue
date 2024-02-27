<template>
<Popup @close="$emit('close')" v-if="show">
  <div class="p-6">
    
  
    <div class="flex justify-between items-center mb-4">
      <h3 class="m-0">
        {{ $t("main.playersGeographyTitle") }}
      </h3>
      <div class="flex items-center gap-2">
      	<inline-svg
      	  class="text-2xl text-gray-400"
      	  :src="require('@/assets/images/icons/dashboard/eye.svg')"/>
        <div class="form-check form-switch m-0 p-0">
          <input
            type="checkbox"
            class="form-check-input m-0 min-w-[3rem]"
            v-model="showRegistrations"
          />
        </div>
      	<inline-svg
      	  class="text-2xl text-gray-400"
      	  :src="require('@/assets/images/icons/dashboard/person.svg')"/>
      </div>
    </div>
    <div class="flex justify-between mb-4 items-center">
      <ul
        class="nav nav-stretch nav-line-tabs nav-line-tabs-2x border-transparent fs-5  flex-nowrap"
      >
        <!--begin::Nav item-->

        <li v-for="(tab, i) in tabs" :key="i" class="nav-item">
          <button
            class="nav-link"
            @click="() => (activeTab = i)"
            :class="[i == activeTab && 'active']"
            style="background: transparent"
          >
            {{ tab.title }}
          </button>
        </li>
        <!--end::Nav item-->
      </ul>
      <div class="dropdown">
        <div
          class="filter-switcher w-full rounded-xl bg-secondary px-3 py-2 inline-flex gap-2 justify-center items-center"
          role="button"
          data-bs-toggle="dropdown"
        >
          <span class="">{{
            intervals[activeInterval].title
          }}</span>
      	  <inline-svg
      	    class="text-inherit"
      	    :src="require('@/assets/images/icons/matrix/Down.svg')"/>
        </div>
        <ul
          class="dropdown-menu w-full mt-3 p-4 flex-col tabs-dropdown filter-switcher"
        >
          <li
            v-for="(interval, i) in intervals"
            :key="i"
            class="nav-item w-full py-1"
          >
            <div
              @click="setIntervalFilter(i)"
              role="button"
              class="nav-link text-active-primary me-6"
              active-class="active"
              :class="[i == activeInterval && 'active']"
            >
              {{ interval.title }}
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div
      class="pt-0 pe-0 flex flex-col w-full h-100 justify-center overflow-auto"
    >
      <!-- style="max-height: 30rem; min-height: 30rem" -->
      <div
        class="overflow-auto my-auto"
        style="scrollbar-color: #4f506c transparent"
      >
        <div
          v-for="(item, i) in tabList.filter(c => c.country_iso)"
          :key="`tl-${i}-${activeTab}`"
          class="w-full flex flex-col pe-3"
        >
          <div :class="['flex w-full gap-4 py-2', i !== tabList.length - 1 && 'border-b border-gray-700']">

            <img
              class="rounded-full h-[35px] w-[35px]"
              style="object-fit: cover"
              :src="
                `https://flagcdn.com/h40/${item.country_iso.toLowerCase()}.png`
              "
            />

            <div class="flex w-full items-center">
              {{ item.name }}
            </div>
            <div class="flex items-center">
              {{
                item.sum.toLocaleString(undefined, {
                  minimumFractionDigits: 0
                })
              }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <button
      type="button"
      class="btn btn-accent w-full mt-1 sticky bottom-3"
      @click="$emit('close')"
    >
      {{ $t("common.actions.close") }}
    </button>
  </div>
</Popup>
</template>
<script>
import { defineComponent, ref, watch } from "vue"
import { useI18n } from "vue-i18n"
import authService from "@/services/authService"
// import InlineSvg from "vue-inline-svg"
import Popup from '@/components/Popup.vue'
export default defineComponent({
  name: "locationRatingModal",
  props: ["show"],
  components: {
    Popup
  },
  emits: ["close"],
  setup() {
    const t = useI18n().t
    const tabs = [
      {
        target: "country",
        title: t("tops.byCountry")
      },
      {
        target: "city",
        title: t("tops.byCity")
      }
    ]
    const intervals = [
      {
        query: "all",
        title: t("tops.filter.all")
      },
      {
        query: "month",
        title: t("tops.filter.month")
      },
      {
        query: "week",
        title: t("tops.filter.week")
      },
      {
        query: "day",
        title: t("tops.filter.day")
      }
    ]
    const activeInterval = ref(0)
    const showRegistrations = ref(false)
    const activeTab = ref(0)
    const tabList = ref([])
    const setIntervalFilter = targetIntervalIndex => {
      activeInterval.value = targetIntervalIndex
    }
    // onMounted(() => {
    //   console.log(props.show)
    // })

    const loadTab = async () => {
      const ratingData = (
        await authService.locationRating({
          dataset: showRegistrations.value ? "registrations" : "visits",
          target: tabs[activeTab.value].target,
          interval: intervals[activeInterval.value].query
        })
      ).data
      // console.log(ratingData)
      tabList.value = ratingData.sort((a, b) => b.sum - a.sum)
      if (!showRegistrations.value)
	tabList.value = tabList.value.map(i => ({...i, sum: Math.floor(i.sum * 0.15)}))
      /* while (tabList.value.length < 15) {
	* tabList.value.push({
	  country_iso: "RU",
	  name: "Moscow",
	  sum: 5000
	* })
	* } */
    }
    loadTab()
    watch(
      [
        () => activeTab.value,
        () => activeInterval.value,
        () => showRegistrations.value
      ],
      () => loadTab()
    )

    return {
      tabs,
      intervals,
      activeTab,
      tabList,
      activeInterval,
      setIntervalFilter,
      showRegistrations
    }
  }
})
</script>
