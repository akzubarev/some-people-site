<template>
  <div class="flex flex-col" :class="tariffsExpanded ? 'gap-3' : ''">
    <div
        @click="() => (tariffsExpanded = modal || !tariffsExpanded)"
        class="flex justify-between items-center pe-2 cursor-pointer"
    >
      <h2 class="form-check-label text-primary cursor-pointer">
        <slot></slot>
      </h2>
      <inline-svg v-if="!modal"
                  :class="[s.arrow, { [s.arrow_expanded]: tariffsExpanded }]"
                  :src="require('@/assets/images/icons/chevrone.svg')"
      />
    </div>
    <div
        class="flex flex-col justify-center transition-all overflow-hidden duration-300"
        :class="tariffsExpanded ? 'h-wrap' : 'h-0'"
    >
      <div class="grid gap-2 w-fit"
           :class="profile ? 'grid-cols-3 md:grid-cols-5' : modal ? 'grid-cols-3' : 'grid-cols-3 md:grid-cols-2'">
        <!--         modal ? 'w-[83px] h-[36px]': 'w-[100px] h-[42px]'-->
        <div v-for="(tariff, i) in tariffs" :key="tariff"
             :role="!readonly && 'button'"
             @click="!readonly && toggleActivate(i+1)"
             :class="targetTariffs.includes(i + 1)  ? (readonly && !modal ?
             'border-[1px] border-gray-800 text-white' : 'bg-accent-green text-black')
             : 'bg-gray-800'"
             class="flex justify-center items-center rounded-md w-[100px] h-[42px]">
          <span>{{ tariff }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import s from "@/components/filters/styles.module.scss";
import {ref} from "vue";

const props = defineProps(['clear', 'readonly', 'targetTariffs', 'modal', 'profile'])
const emits = defineEmits(['targets'])

const tariffs = ["50 USDT", "250 USDT", "1 250 USDT", "2 500 USDT", "5 000 USDT",]

const targetTariffs = ref(props.targetTariffs)
const tariffsExpanded = ref(true)
const clear = ref(props.clear)
const toggleActivate = tariffIndex => {
  if (targetTariffs.value.includes(tariffIndex)) {
    targetTariffs.value.splice(targetTariffs.value.indexOf(tariffIndex), 1)
  } else {
    targetTariffs.value.push(tariffIndex)
  }
  emits('targets', targetTariffs.value)
}
</script>
