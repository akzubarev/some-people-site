<template>
  <div class="!h-fit card md:max-w-[290px]">
    <div class="card-body">
      <BaseFilters
          :key="clearToggle" :clear="clearToggle"
          :filters-config="filtersConfigRef"
          @change="f => {
              filters.onlyActive = f.onlyActive
              filters.onlySubscribed =  f.onlySubscribed
            $emit('change', result_filters)
          }">
        <DepthFilter :key="clearToggle" :depth="depth" @change="(d) => {
          depth=d; $emit('change', result_filters) }"
        />

        <TariffsFilter :key="clearToggle"
                       :target-tariffs="targetTariffs"
                       @targets="(target)=>{
            targetTariffs=target;$emit('change', result_filters) }"
        >
          {{ $t("matrix.tree.activeTariffs") }}
        </TariffsFilter>
        <!--        <MissionsFilter :key="clearToggle" :target-missions="targetMissions"-->
        <!--                        @targets="(target)=>{-->
        <!--            targetMissions=target;$emit('change', result_filters) }"-->
        <!--        />-->
        <!--        <div :class="s.button_wrapper" v-if="filters_changed">-->
        <!--          <button-->
        <!--              :class="s.button" class="btn btn-outline btn-outline-primary"-->
        <!--              @click="() => {-->
        <!--              filters.onlyActive = defaultFilters.onlyActive-->
        <!--              filters.onlySubscribed = defaultFilters.onlySubscribed-->
        <!--              targetMissions = defaultFilters.targetMissions-->
        <!--              depth = defaultFilters.depth-->
        <!--              clearToggle = !clearToggle-->
        <!--              $emit('change', result_filters)-->
        <!--            }"-->
        <!--          >-->
        <!--            {{ $t("common.actions.clear") }}-->
        <!--          </button>-->
        <!--        </div>-->
      </BaseFilters>
    </div>
  </div>
</template>

<script setup>

import {computed, ref, toRaw} from "vue";
import {useI18n} from "vue-i18n";
import DepthFilter from "@/components/filters/DepthFilter.vue";
import BaseFilters from "@/components/filters/BaseFilters.vue";
import TariffsFilter from "@/components/filters/TariffsFilter.vue";

const {t} = useI18n()
const emit = defineEmits(['change'])

const defaultFilters = {
  targetTariffs: [],
  // onlyActive: null,
  // onlySubscribed: null,
  depth: 1
}

const targetTariffs = ref(defaultFilters.targetTariffs)
const depth = ref(defaultFilters.depth)
const clearToggle = ref(false)

const filtersConfig = [
  // {
  //   title: t('user.subscription'), key: 'onlySubscribed',
  //   expanded: true, value: defaultFilters.onlySubscribed,
  //   choices: [
  //     {title: t("user.active"), value: true,},
  //     {title: t("user.notActive"), value: false,},
  //   ],
  // },
  // {
  //   title: t('matrix.tree.missions'), key: 'onlyActive',
  //   expanded: true, value: defaultFilters.onlyActive,
  //   choices: [
  //     {title: t("matrix.tree.activated"), value: true},
  //     {title: t("matrix.tree.notActivated"), value: false},
  //   ],
  // },
]

const filters = ref({})
const filtersConfigRef = ref(JSON.parse(JSON.stringify(filtersConfig)))

// const filters_changed = computed(() => {
//   return filters.value.onlyActive !== defaultFilters.onlyActive ||
//       filters.value.onlySubscribed !== defaultFilters.onlySubscribed ||
//       depth.value !== defaultFilters.depth ||
//       toRaw(targetTariffs.value) !== defaultFilters.targetTariffs
// })

const result_filters = computed(() => {
  return {
    // onlyActive: filters.value.onlyActive,
    // onlySubscribed: filters.value.onlySubscribed,
    depth: depth.value,
    targetTariffs: targetTariffs.value
  }
})


</script>