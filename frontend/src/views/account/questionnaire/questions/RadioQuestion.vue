<template>
  <div class="flex flex-col cursor-pointer gap-3">
    <div v-for="(option, i) in question.choices" :key="option">
      <div class="form-check">
        <input @change="change(option)" v-model="res" type="radio"
               class="form-check-input w-[20px]" :id="`radio${question.id}${i}`"
               :value="option" :name="'radio' + question.id">
        <label :for="`radio${question.id}${i}`" class="text-medium text-content-secondary w-[95%]">
          {{ option }}
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue";

const emit = defineEmits(['change', 'readonly'])
const props = defineProps({
      defaultValue: {type: String, default: ""},
      question: {default: {id: 1, choices: []}},
      readonly: {type: Boolean, default: false},
    }
)
const res = ref(props.defaultValue)
const change = (option) => {
  if (!props.readonly) {
    res.value = option;
    emit('change', res.value)
  }
}
</script>
