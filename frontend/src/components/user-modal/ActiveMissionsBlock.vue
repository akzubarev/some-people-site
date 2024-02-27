<template>
  <div class="flex flex-col gap-3">
    <template v-for="(mission, i) in missions" :key="mission.title">
      <span class="text-[var(--dark-text-color)]">{{ mission.title }}</span>
      <div class="flex gap-2 flex-wrap">
        <div v-for="j in mission.count" :key="mission.title + j"
             :role="!readonly && 'button'"
             @click="!readonly && toggleActivate(j + i * missions[0].count - 1)"
             :class="activated.includes(j + i * missions[0].count - 1)
          ? (readonly ? 'border-[1px] border-gray-800 text-white' : 'bg-accent-green text-black')
          : 'bg-gray-800'"
             class="flex justify-center items-center rounded-md w-[42px] h-[42px]">
          <span>{{ j }}</span>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import {ref, watch} from 'vue'


const missions = [
  {title: 'Camp', count: 4},
  {title: 'Energy', count: 12},
]
const emit = defineEmits(['targets'])
const props = defineProps(['clear', 'readonly', 'opened_matrix', 'showSubscription'])
const activated = ref(props.opened_matrix?.map(v => +v) || [])

watch(() => props.clear, () => activated.value = [])

const toggleActivate = index => {
  if (activated.value.includes(index)) {
    activated.value.splice(activated.value.indexOf(index), 1)
  } else {
    activated.value.push(index)
  }
  // console.log(Array.from(activated.value))
  emit('targets', activated.value)
}
</script>
