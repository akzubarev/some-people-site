<template>
  <div class="flex flex-col gap-3 cursor-pointer min-w-[100px]">
    <div @click="() => expanded = !expanded"
         class="flex justify-between items-center pe-2">
      <h2 class="text-muted font-normal text-xl">
        {{ $t("common.filter") }} </h2>
      <inline-svg
          :class="['text-[.55rem] transition-all w-[16px] h-[16px] text-[var(--dark-text-color)]',
          expanded ? 'rotate-180' : 'rotate-0']"
          :src="require('@/assets/images/icons/chevrone.svg')"/>
    </div>
    <div v-if="!expanded" @click="() => expanded = !expanded"
         class="flex flex-wrap items-center gap-1">
      <h3 class="font-normal text-gray-400 text-sm">
        {{ filtersStr(filters) }} </h3>
    </div>

    <div v-if="expanded" class="flex flex-col gap-3">
      <div
          v-for="(filter, i) in filters" :key="filter"
          @click="() => filter.expanded = !filter.expanded"
          class="flex flex-col cursor-pointer"
          :class="i !== filters.length - 1 ? ' border-bottom' : ''">
        <div class="flex justify-between items-center pe-2">
          <h2 class="text-muted font-normal">{{ filter.title }}</h2>
          <inline-svg
              :class="['text-[.55rem] transition-all w-[16px] h-[16px] text-[var(--dark-text-color)]',
          filter.expanded ? 'rotate-180' : 'rotate-0']"
              :src="require('@/assets/images/icons/chevrone.svg')"/>
        </div>
        <div v-if="!filter.expanded" class="flex flex-wrap items-center">
          <h3 class="font-normal text-gray-400 text-sm">{{
              filter.choices.find(element => element.value === filter.value)?.title
            }} </h3>
        </div>
        <div
            class="flex flex-col justify-start mt-4 gap-4 transition-all overflow-y-auto duration-300 max-h-[30vh]"
            :class="filter.expanded ? `pb-4 pt-1` : '!h-0 overflow-hidden'"
            :style="`height: ${2.8 * filter.choices.length}rem`">
          <template v-for="(choice, j) in filter.choices" :key="choice">
            <!-- JSX is simply better at this -->
            <div v-if="filter.type == 'flags'" class="flex justify-between"
                 @click="() => {
                filter.value = choice.value
                $emit('change', computedFilter)
              }">
              <div class="flex gap-2">
                <inline-svg v-if="choice.value === 'all'"
                            :src="require('@/assets/images/icons/Circles.svg')"/>
                <img v-else class="rounded-full h-[24px] w-[24px] object-cover"
                     :src="`https://flagcdn.com/h40/${choice.value.toLowerCase()}.png`"/>
                <label class="form-check-label text-primary cursor-pointer"
                       :for="'radio' + filter.key + j">
                  {{ choice.title }}
                </label>
              </div>
              <div class="relative pe-2">
                <input v-model="filter.value"
                       class="visibility-hidden opacity-0" type="radio"
                       :value="choice.value" :name="'radio' + filter.key"
                       :id="'radio' + filter.key + j">
                <inline-svg v-if="filter.value === choice.value"
                            class=" absolute text-[1.5rem] top-[3px]"
                            :src="require('@/assets/images/icons/matrix/Check.svg')"/>
              </div>
            </div>
            <div v-else class="form-check flex gap-3" @click="() => {
                filter.value = choice.value
                $emit('change', computedFilter)
              }">
              <input @change="() => {
              filter.value = choice.value
              $emit('change', computedFilter)
            }" v-model="filter.value"
                     class="form-check-input !w-[1.5rem] !h-[1.5rem]"
                     type="radio"
                     :value="choice.value" :name="'radio' + filter.key"
                     :id="'radio' + filter.key + j">
              <label class="form-check-label text-primary cursor-pointer"
                     :for="'radio' + filter.key + j">
                {{ choice.title }}
              </label>
            </div>
          </template>
        </div>
      </div>
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, watch} from "vue"
import {useI18n} from "vue-i18n"


const emit = defineEmits(['change'])
const props = defineProps(['filtersConfig', 'clear'])
const {t} = useI18n()
const filters = ref(props.filtersConfig)
const expanded = ref(false)
const computedFilter = computed(() => {
  return filters.value.reduce((acc, val) => Object.assign(acc, {[val.key]: val.value}), {})
})

const filtersStr = (filters) => {
  const titles = []
  filters.forEach(function (filter, i) {
    const title = filter.choices.find(element => element.value === filter.value)?.title
    if (title != null)
      titles.push(title)
  });
  return titles.join(", ")
}

watch(props.clear, () => {
  filters.value = props.filtersConfig
})

</script>
