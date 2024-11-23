<template>
  <div class="flex gap-3" :class="horizontal ? 'flex-row':'flex-col'">
    <div class="flex flex-col gap-1">
      <div class="flex flex-col text-medium text-content-secondary font-semibold"> {{ question.title }}</div>
      <div class="text-medium text-content-secondary-shadowed"> {{ question.description }}</div>
    </div>
    <Field v-if="question.type==='line'" v-model="answer"
           class="form-input text-content-secondary bg-white" type="text"
           :name="field_name" placeholder="Строка..."
           @change="$emit('change', field_name, answer)"
           :readonly="readonly"
    />
    <Field v-if="question.type==='paragraph'" v-model="answer"
           class="form-input text-content-secondary bg-white h-[150px]" type="text"
           :name="field_name" placeholder="Абзац..."
           @change="$emit('change', field_name, answer)"
           :readonly="readonly" as="textarea"
    />
    <RadioQuestion
        v-if="question.type==='single_choice'" :question="question"
        :default-value="defaultValue ? defaultValue[question.id] : null" :readonly="readonly"
        @change="(value) => { answer=value; $emit('change', field_name, answer) }"
    />
    <CheckboxQuestion
        v-if="question.type==='multiple_choice'" :question="question"
        :default-value="!!defaultValue ? defaultValue[question.id] : null" :readonly="readonly"
        @change="(value) => { answer=value; $emit('change', field_name, answer) }"
    />
    <ScaleQuestion
        v-if="question.type==='scale'" :question="question"
        :default-value="!!defaultValue ? defaultValue[question.id] : null" :readonly="readonly"
        @change="(value) => { answer=value; $emit('change', field_name, answer) }"
    />
    <MatrixQuestion
        v-if="question.type.includes('matrix')"
        :question="question" :checkbox="question.type=='matrix_checkbox'"
        :default-value="!!defaultValue ? defaultValue[question.id] : null" :readonly="readonly"
        @change="(value) => { answer=value; $emit('change', field_name, answer) }"
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
import {ref} from "vue";
import {Field} from "vee-validate"
import RadioQuestion from "@/views/account/questionnaire/questions/RadioQuestion.vue";
import CheckboxQuestion from "@/views/account/questionnaire/questions/CheckboxQuestion.vue";
import ScaleQuestion from "@/views/account/questionnaire/questions/ScaleQuestion.vue";
import MatrixQuestion from "@/views/account/questionnaire/questions/MatrixQuestion.vue";

const emit = defineEmits(['change'])
const props = defineProps([
  "horizontal", "question", "errors", "defaultValue", "readonly", "showErrors"
])
const field_name = `question_${props.question.id}`
const answer = ref((props.defaultValue ? props.defaultValue[props.question.id] : null) || "")
const progress = ref([])
emit("change", field_name, answer.value)

</script>
