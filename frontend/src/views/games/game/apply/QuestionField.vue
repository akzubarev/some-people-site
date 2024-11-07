<template>
  <div class="flex flex-wrap gap-1"
       :class="horizontal ? 'flex-row':'flex-col'">
    <label class="flex items-center"
           :class="horizontal && 'basis-full lg:basis-1/3'">
      {{ question.title }}
    </label>
    <div class="flex items-center text-content-disabled"
         :class="horizontal && 'basis-full lg:basis-1/3'">
      {{ question.description }}
    </div>
    <div class="flex flex-col gap-1" :class="horizontal && 'basis-full lg:basis-2/3'">
      <Field v-if="question.type==='line'" v-model="answer"
             class="form-input" type="text" :name="field_name" placeholder=""
             @change="$emit('change', field_name, answer)"
             :readonly="readonly"
      />
      <Field v-if="question.type==='paragraph'" v-model="answer"
             class="form-input h-[150px]" type="text" :name="field_name" placeholder=""
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
          :default-value="defaultValue ? defaultValue[question.id] : null" :readonly="readonly"
          @change="(value) => { answer=value; $emit('change', field_name, answer) }"
      />
      <ScaleQuestion
          v-if="question.type==='scale'" :question="question"
          :default-value="defaultValue ? defaultValue[question.id] : null" :readonly="readonly"
          @change="(value) => { answer=value; $emit('change', field_name, answer) }"
      />
      <MatrixQuestion
          v-if="question.type==='matrix'" :question="question"
          :default-value="defaultValue ? defaultValue[question.id] : null" :readonly="readonly"
          @change="(value) => { answer=value; $emit('change', field_name, answer) }"
      />
      <div class="fv-plugins-message-container">
        <div class="fv-help-block">
          <span class="text-red-700">{{
              errors[field_name] || (!answer && showErrors ? "Ответ не может быть пустым" : "")
            }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue";
import {Field} from "vee-validate"
import RadioQuestion from "@/views/games/game/apply/questions/RadioQuestion.vue";
import CheckboxQuestion from "@/views/games/game/apply/questions/CheckboxQuestion.vue";
import ScaleQuestion from "@/views/games/game/apply/questions/ScaleQuestion.vue";
import MatrixQuestion from "@/views/games/game/apply/questions/MatrixQuestion.vue";

const emit = defineEmits(['change'])
const props = defineProps([
  "horizontal", "question", "errors", "defaultValue", "readonly", "showErrors"
])
const field_name = `question_${props.question.id}`
const answer = ref((props.defaultValue ? props.defaultValue[props.question.id] : null) || "")
const progress = ref([])
emit("change", field_name, answer.value)

</script>
