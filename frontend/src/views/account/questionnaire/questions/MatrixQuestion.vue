<template>
  <div class="flex flex-col w-full gap-6">
    <div class="flex flex-row items-center gap-3 md:gap-6">
      <div class="w-full min-w-[40%] items-center"/>
      <div v-for="option in question.choices[0]" :key="option"
           class="w-full items-center text-center text-medium text-content-secondary">
        {{ option }}
      </div>
    </div>
    <div class="flex flex-row w-full items-center rounded-xl gap-3 md:gap-6"
         v-for="(option, i) in question.choices[1]" :key="option">
      <div class="w-full min-w-[40%] text-medium text-content-secondary"> {{ option }}</div>
      <div class="flex w-full cursor-pointer justify-center items-center" v-for="(_, j) in question.choices[0]"
           :key="j" @click="onInput(i, j)">
        <input
            class="form-check-input" :id="`input${question.id}${i}${j}`" :name="`input${question.id}${i}`"
            :type="checkbox? 'checkbox' : 'radio'" :checked="res[i][j]"
        />
      </div>
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
const onInput = (i, j) => {
  if (!props.readonly) {
    if (!props.checkbox) {
      res.value[i] = props.question.choices[0].map(() => false)
      res.value[i][j] = true
    } else
      res.value[i][j] = !res.value[i][j]
    emit('change', answer.value)
  }
}
</script>
