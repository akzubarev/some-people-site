<template>
  <Form class="form flex flex-col h-full gap-6 md:bg-bg-transparent-white overflow-y-auto no-scrollbar px-6 md:px-0"
        novalidate="novalidate" @submit="onSubmit">
    <div class="flex flex-col gap-6">
      <div class="text-large font-bold text-content-secondary uppercase"> {{
          $t('application.questionnaire_title')
        }}
      </div>
      <div class="text-sm font-semibold text-content-secondary-shadowed whitespace-pre-wrap"> {{
          $t('application.questionnaire_description')
        }}
      </div>
    </div>
    <div class="flex flex-col gap-medium">
      <QuestionField
          v-for="question in questions" @change="answerUpdate"
          :key="`${question.id} ${default_answers[question.id]}`"
          :question="question" :horizontal="false"
          :readonly="!!userId" :show-errors="showErrors" :errors="errors"
          :unfilled="application.answers?.unfilled?.includes(question.id)"
          :default-value="default_answers[question.id]"
      />
      <div class="flex w-full md-6"/>
    </div>
    <!--    <button ref="submitButton" type="submit" class="btn-gradient w-full text-center text-xl">-->
    <!--      {{ 'Сохранить' }}-->
    <!--    </button>-->
  </Form>
</template>

<script setup lang="ts">
import {computed, ref} from "vue"
import {Form} from "vee-validate"
import {useStore} from "vuex"
import {useRouter} from "vue-router"
import formhelper from "@/core/helpers/form"
import QuestionField from "@/views/account/questionnaire/QuestionField.vue";
import gamesService from "@/services/gamesService";

const store = useStore()
const router = useRouter()
const form = formhelper()
const {errors} = form

const props = defineProps(["game_alias", "userId"])
const showErrors = ref(false)
const game_alias = props.game_alias

const user_id = computed(() => props.userId || store.getters['auth/user'].id)
const application = computed(() => store.getters["games/application"])
const questions = computed(() => store.getters["games/questions"].filter(question => question.order > 0))

const getQAnswers = (answers) => {
  return Object.fromEntries(Object.entries(answers).filter((q_id, v) => q_id > 0 && !!v))
}

const answers = ref(getQAnswers(application.value.answers?.values || {}))
const default_answers = computed(() => application.value.answers?.values || {})

const answerUpdate = (field_name, answer) => {
  answers.value[field_name] = answer
}

const loadData = () => {
  gamesService.application(user_id.value, game_alias).then(({data}) => {
    store.dispatch("games/setApplication", data)
    answers.value = getQAnswers(data.answers.values)
  })
  gamesService.questions(props.game_alias).then(({data}) => {
    store.dispatch("games/setQuestions", data)
  })
}

const onSubmit = (values) => {
  const answersToSend = {...answers.value, game_alias: game_alias}
  showErrors.value = true
  form.send(async () => {
    await gamesService.apply(answersToSend)
    loadData()
  })
}
const onLeave = () => {
  const answersToSend = {...answers.value, game_alias: game_alias}
  form.send(async () => {
    await gamesService.apply(answersToSend)
  })
}

window.addEventListener('beforeunload', onLeave)
</script>
