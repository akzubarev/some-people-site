<template>
  <Form class="form flex flex-col h-full gap-6 p-6 bg-bg-transparent-white overflow-y-auto no-scrollbar"
        novalidate="novalidate" @submit="onSubmit">
    <ActionModal
        v-if="showModal" type="lock"
        @close="() => {showModal = false}"
        @submit="() => {showModal = false}"
        title="Ответьте на все вопросы, чтобы отправить анкету." :buttonText="$t('common.actions.ok')">
    </ActionModal>
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
          v-for="question in questions" :key="question"
          :question="question" :horizontal="false" :value="answers"
          @change="answerUpdate" :errors="errors"
          :default-value="application.answers"
          :readonly="!!userId" :show-errors="showErrors"
      />
    </div>
    <button ref="submitButton" type="submit" class="btn-gradient w-full text-center text-xl">
      {{ !!application ? 'Сохранить' : 'Отправить' }} заявку
    </button>
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
import ActionModal from "@/components/ActionModal.vue";

const store = useStore()
const router = useRouter()
const progress = ref([])
const form = formhelper()
const {errors} = form

const props = defineProps(["game_alias", "userId"])
const questions = ref([])
const showErrors = ref(false)
const showModal = ref(false)
const answers = ref({})
const application = ref({
  id: 1, status: "approved", answers: [], price: 0, payed: 0,
})
const game_alias = props.game_alias
const user_id = computed(() => props.userId || store.getters['auth/user'].id)
gamesService.application(user_id.value, game_alias).then(({data}) => {
  application.value = data
  gamesService.questions(game_alias).then(({data}) => {
    questions.value = data.filter(question => question.order > 0)
  })
})

const answerUpdate = (question, answer) => {
  answers.value[question] = answer
  if (!!answer && !progress.value.includes(question)) {
    progress.value.push(question)
  } else if (!answer && progress.value.includes(question)) {
    progress.value.splice(progress.value.indexOf(question), 1)
  }
}

const onSubmit = (values) => {
  answers.value = {...values, ...answers.value, game_alias: game_alias}
  showErrors.value = true
  form.send(async () => {
    if (Object.values(answers.value).includes(null) || Object.values(answers.value).includes("")) {
      showModal.value = true
      return
    }
    await gamesService.apply({game_alias: game_alias, ...answers.value})
    gamesService.application(user_id.value, game_alias).then(({data}) => {
      application.value = data
    })
  })
}
</script>
