<template>
  <div v-for="(option, i) in question.choices" :key="option">
    <div class="flex flex-col cursor-pointer gap-1"
         @click="() => { if (!readonly) {res[i] = !res[i]; $emit('change',answer)}}">
      <div class="form-check flex gap-3">
        <input type="checkbox" class="form-check-input m-0" :name="'checkbox' + question.id"
               :checked="res[i]" :id="`checkbox${question.id}${i}`">
        <label class="text-content-primary" :for="`checkbox${question.id}${i}`">
          {{ option }}
        </label>
      </div>
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
    }
)
const res = ref(props.defaultValue ?
    props.question.choices.map((choice) => props.defaultValue.includes(choice))
    : props.question.choices.map((choice) => false)
)
const answer = computed(() => {
  return props.question.choices.filter((choice, i) => res.value[i])
})

</script>
