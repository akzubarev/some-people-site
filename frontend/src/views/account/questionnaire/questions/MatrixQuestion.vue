<template>
  <div class="flex flex-col gap-6">
    <div class="flex flex-row items-center gap-3 md:gap-6">
      <div class="w-full min-w-[40%] items-center"/>
      <div v-for="option in question.choices[0]" :key="option"
           class="w-full items-center text-center text-medium text-content-secondary">
        {{ option }}
      </div>
    </div>
    <div class="flex flex-row items-center rounded-xl gap-3 md:gap-6"
         v-for="(option, i) in question.choices[1]" :key="option">
      <div class="w-full min-w-[40%] text-medium text-content-secondary"> {{ option }}</div>
      <input
          class="form-check-input w-full cursor-pointer"
          v-for="(_, j) in question.choices[0]" :key="j"
          :id="`input${question.id}${i}${j}`" :name="`input${question.id}${i}`"
          :type="checkbox? 'checkbox' : 'radio'" :checked="res[i][j]"
          @click="() => { if (!readonly) {res[i][j] = !res[i][j]; $emit('change', answer)}}"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
import {computed, ref} from "vue";

const emit = defineEmits(['change'])
const props = defineProps({
  defaultValue: {type: Array, default: []},
  question: {type: Object, default: {id: 1, choices: []}},
  readonly: {type: Boolean, default: false},
  checkbox: {type: Boolean, default: false},
})
const res = ref(props.defaultValue?.length > 0 ?
    props.question.choices[1].map(
        (question, i) => props.question.choices[0].map((choice) => props.defaultValue[i].includes(choice))
    ) : props.question.choices[1].map(() => props.question.choices[0].map(() => false))
)
const answer = computed(() => {
  return props.question.choices[1].map(
      (question, i) => props.question.choices[0].filter((choice, j) => res.value[i][j])
  )
})
</script>
