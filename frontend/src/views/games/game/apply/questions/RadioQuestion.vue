<template>
  <div v-for="(option, i) in question.choices" :key="option">
    <div class="flex flex-col cursor-pointer gap-1">
      <div class="form-check flex gap-3">
        <input
            @change="change(option)" v-model="res" type="radio"
            class="form-check-input !w-[1.5rem] !h-[1.5rem]"
            :value="option" :name="'radio' + question.id"
            :id="`radio${question.id}${i}`">
        <label :for="`radio${question.id}${i}`">
          {{ option }}
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";

const emit = defineEmits(['change', 'readonly'])
const props = defineProps({
      defaultValue: {type: String, default: ""},
      question: {type: Object, default: {id: 1, choices: []}},
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
