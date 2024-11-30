<template>
  <div class="flex flex-col cursor-pointer gap-3">
    <div v-for="(option, i) in question.choices" :key="option">
      <div class="form-check" @click="() => { if (!readonly) {res[i] = !res[i]; $emit('change',answer)}}">
        <input type="checkbox" class="form-check-input m-0 w-[20px]" :name="'checkbox' + question.id"
               :checked="res[i]" :id="`checkbox${question.id}${i}`">
        <label :for="`checkbox${question.id}${i}`" class="text-medium text-content-secondary w-[95%]">
          {{ option }}
        </label>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import {computed, ref} from "vue";

const emit = defineEmits(['change'])
const props = defineProps({
      defaultValue: {type: Array, default: []},
      question: {default: {id: 1, choices: []}},
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
