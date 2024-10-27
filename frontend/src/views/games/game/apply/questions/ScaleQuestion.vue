<template>
  <div class="flex flex-col gap-1">
    <ProgressBar class="h-[8px]" :progress="scale_fill"/>
    <div class="flex flex-row justify-between p-3">
      <div v-for="(option, i) in question.choices" :key="option">
        <div class="flex flex-col cursor-pointer gap-1">
          <div class="form-check flex gap-3">
            <input
                @change="change(option, i)" v-model="res" type="radio"
                class="form-check-input !w-[1.5rem] !h-[1.5rem]"
                :value="option" :name="'radio' + question.id"
                :id="`radio${question.id}${i}`">
            <label class="text-content-primary cursor-pointer" :for="`radio${question.id}${i}`">
              {{ option }}
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";
import ProgressBar from "@/components/progressbar/ProgressBar.vue";

const emit = defineEmits(['change', 'readonly'])
const scale_fill = ref(0)
const props = defineProps({
      defaultValue: {type: String, default: ""},
      question: {type: Object, default: {id: 1, choices: []}},
      readonly: {type: Boolean, default: false},
    }
)
const res = ref(props.defaultValue)
const change = (option, i) => {
  if (!props.readonly) {
    res.value = option;
    scale_fill.value = 100 * i / (props.question.choices.length - 1)
    emit('change', res.value)
  }
}
</script>
