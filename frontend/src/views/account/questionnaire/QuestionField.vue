<template>
  <div class="flex gap-3" :class="horizontal ? 'flex-row':'flex-col'">
    <div class="flex flex-col gap-1">
      <div class="flex flex-row gap-2 items-center">
        <div class="text-medium text-content-secondary font-semibold w-fit max-w-[95%]"> {{ question.title }}</div>
        <div v-if="unfilled" class="h-2 w-2 bg-bg-transparent rounded-full"/>
      </div>
      <div class="text-medium text-content-secondary-shadowed"> {{ question.description }}</div>
    </div>
    <Field v-if="question.type==='line'" v-model="answer"
           class="form-input text-content-secondary bg-white" type="text"
           :name="field_name" placeholder="Строка..." :readonly="readonly"
           @change="$emit('change', field_name, answer, true)"
    />
    <Field v-if="question.type==='paragraph'" v-model="answer" as="textarea"
           class="form-input text-content-secondary bg-white h-[150px]" type="text"
           :name="field_name" placeholder="Абзац..." :readonly="readonly"
           @change="$emit('change', field_name, answer, true)"
    />
    <RadioQuestion
        v-if="question.type==='single_choice'" :question="question"
        :default-value="defaultValue ? defaultValue : null" :readonly="readonly"
        @change="(value) => { answer=value; $emit('change', field_name, answer, true) }"
    />
    <CheckboxQuestion
        v-if="question.type==='multiple_choice'" :question="question"
        :default-value="!!defaultValue ? defaultValue : null" :readonly="readonly"
        @change="(value) => { answer=value; $emit('change', field_name, answer, true) }"
    />
    <ScaleQuestion
        v-if="question.type==='scale'" :question="question"
        :default-value="!!defaultValue ? defaultValue : null" :readonly="readonly"
        @change="(value) => { answer=value; $emit('change', field_name, answer, true) }"
    />
    <MatrixQuestion
        v-if="question.type.includes('matrix')"
        :question="question" :checkbox="question.type=='matrix_checkbox'"
        :default-value="!!defaultValue ? defaultValue : null" :readonly="readonly"
        @change="(value) => {answer=value; $emit('change', field_name, answer, true)}"
    />
    <div class="fv-plugins-message-container" v-if="!!errors[field_name]">
      <div class="fv-help-block">
        <div class="text-red-700">{{
            errors[field_name] || (!answer && showErrors ? "Ответ не может быть пустым" : "")
          }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {Field} from "vee-validate"
import RadioQuestion from "@/views/account/questionnaire/questions/RadioQuestion.vue";
import CheckboxQuestion from "@/views/account/questionnaire/questions/CheckboxQuestion.vue";
import ScaleQuestion from "@/views/account/questionnaire/questions/ScaleQuestion.vue";
import MatrixQuestion from "@/views/account/questionnaire/questions/MatrixQuestion.vue";
import {ref} from "vue";

const emit = defineEmits(['change'])
const props = defineProps([
  "horizontal", "question", "errors", "defaultValue", "readonly", "showErrors", "unfilled",
])
const answer = ref(props.defaultValue || "")
const field_name = `question_${props.question.id}`
emit("change", field_name, answer.value, false)
</script>
