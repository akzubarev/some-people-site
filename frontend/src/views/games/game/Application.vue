<template>
  <div class="flex flex-col gap-3 mt-48">
    <div class="card flex flex-col gap-1 p-6">
      <div class="flex flex-row items-center justify-between gap-3">
        <div class="whitespace-pre-wrap" v-if="application.price">
          Взнос {{ application.payed }} / {{ application.price }}
        </div>
        <div class="flex flex-row items-center gap-3">
          <div class="whitespace-pre-wrap"> Статус: {{
              {
                "pending": "Подана",
                "discussing": "Обсуждается",
                "confirmed": "Принята",
                "declined": "Отклонена",
                "deleted": "Удалена"
              }[application.status] || "Не подана"
            }}
          </div>
          <button class="btn btn flex items-center bg-white hover:bg-gray-500
              text-center text-black !p-2">
            Удалить
          </button>
        </div>
      </div>
      <div class="flex flex-row items-center justify-between gap-3">
        <div class="whitespace-no-wrap w-[20%]">
          Заполнено {{ progress.length * 100 / questions.length}}%
        </div>
        <ProgressBar
            :class="progress.length ? 'h-[8px]' : '!h-0'"
            color="linear-gradient(to right, #56405f, #44405f)"
            :progress="progress.length * 100 / questions.length"
        />
      </div>
    </div>
    <Form class="card form w-full p-6" novalidate="novalidate"
          @submit="onSubmit">
      <div class="flex flex-col gap-6">
        <div class="grid grid-cols-1 gap-3 !h-[390px] overflow-auto">
          <QuestionField
              v-for="question in questions" :key="question"
              :question="question" :horizontal="false" :value="answers"
              @change="answerUpdate" :errors="errors"
              :default-value="application.answers"
              :readonly="!!userId" :show-errors="showErrors"
          />
        </div>

        <div class="text-center">
          <button id="kt_sign_up_submit" ref="submitButton" type="submit"
                  class="btn btn-lg btn-accent w-full">
            <span class="indicator-label">
              {{ !!application ? 'Сохранить' : 'Отправить' }} заявку
            </span>
            <span class="indicator-progress">
              <span
                  class="spinner-border spinner-border-sm align-middle ms-2"/>
            </span>
          </button>
        </div>
      </div>
    </Form>
  </div>
</template>

<script setup>
import {ref} from "vue"
import {Form} from "vee-validate"
import ProgressBar from "@/components/progressbar"
import {useStore} from "vuex"
import {useRouter} from "vue-router"
import formhelper from "@/core/helpers/form"
import QuestionField from "@/views/games//game/apply/QuestionField.vue";
import gamesService from "@/services/gamesService";

const store = useStore()
const router = useRouter()
const progress = ref([])
const form = formhelper()
const {errors} = form


const props = defineProps(["alias", "userId"])
const questions = ref([])
const showErrors = ref(false)
const answers = ref({})
const application = ref({
  id: 1, status: "approved", answers: [], price: 0
})
const game_alias = props.alias
const user_id = props.userId || store.getters['auth/user'].id
gamesService.application(user_id, game_alias).then(({data}) => {
  application.value = data
  gamesService.questions(game_alias).then(({data}) => {
    questions.value = data
  })
})

const answerUpdate = (question, answer) => {
  answers.value[question] = answer
  if (!!answer && !progress.value.includes(question)) {
    progress.value.push(question)
  } else if (!answer && progress.value.includes(question)) {
    progress.value.splice(progress.value.indexOf(question), 1)
  }
  console.log(progress.value)
}

const onSubmit = (values) => {
  answers.value = {...values, ...answers.value, game_alias: game_alias}
  showErrors.value = true
  form.send(async () => {
    if (Object.values(answers.value).includes(null) || Object.values(answers.value).includes(""))
      throw new Error("Fields contain nulls")
    const data = (await gamesService.apply({
      game_alias: game_alias, ...answers.value
    }))["data"]
    gamesService.application(user_id, game_alias).then(({data}) => {
      application.value = data
    })
  })
}
</script>
