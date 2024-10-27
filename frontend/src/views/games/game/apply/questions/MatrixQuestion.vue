<template>
  <div class="flex flex-col gap-3">
    <div class="flex flex-row items-center gap-3">
      <div class="w-full items-center"/>
      <div v-for="option in question.choices[0]" :key="option"
           class="w-full items-center text-center text-content-primary">
        {{ option }}
      </div>
    </div>
    <div class="flex flex-row items-center gap-3" v-for="(option, i) in question.choices[1]" :key="option">
      <div class="w-full text-content-primary">
        {{ option }}
      </div>
      <input v-for="(_, j) in question.choices[0]" :key="j" :id="`checkbox${question.id}${i}`" type="checkbox"
             class="form-check-input w-full cursor-pointer" :name="'checkbox' + question.id" :checked="res[i]"
             @click="() => { if (!readonly) {res[i][j] = !res[i][j]; $emit('change',answer)}}"
      />
    </div>
  </div>
</template>
<script setup>
import {computed, ref} from "vue";

const emit = defineEmits(['change'])
const props = defineProps({
  defaultValue: {type: Array, default: []},
  question: {type: Object, default: {id: 1, choices: []}},
  readonly: {type: Boolean, default: false},
})
const res = ref(props.defaultValue ?
    props.question.choices[1].map(
        (question, i) => props.question.choices[0].map((choice) => props.defaultValue[i].includes(choice))
    ) : props.question.choices[1].map(props.question.choices[0].map(() => false))
)
const answer = computed(() => {
  return props.question.choices[1].map(
      (question, i) => props.question.choices[0].filter((choice, j) => res.value[i][j])
  )
})

</script>
