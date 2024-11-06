<template>
  <div class="flex flex-col gap-3 mt-48">
    <div class="card flex flex-col gap-1 p-6">
      <div class="flex flex-row w-full items-center justify-between gap-3">
        <div class="whitespace-pre-wrap">
          Взнос {{ application.price ? `${application.payed} / ${application.price}` : 'не объявлен' }}
        </div>
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
        <button class="btn-gradient text-center">Удалить</button>
      </div>
      <div class="flex flex-row items-center justify-between gap-3">
        <div class="whitespace-no-wrap w-[20%]">
          Заполнено {{ Math.ceil(100 * progress.length / questions.length) }}%
        </div>
        <ProgressBar class="h-[8px]" :progress="100 * progress.length / questions.length"/>
      </div>
    </div>
    <Form class="card form w-full h-full p-6 no-scrollbar" novalidate="novalidate" @submit="onSubmit">
      <div class="flex flex-col gap-6 no-scrollbar">
        <div class="grid grid-cols-1 gap-3 !h-[390px] overflow-auto no-scrollbar">
          <QuestionField
              v-for="question in questions" :key="question"
              :question="question" :horizontal="false" :value="answers"
              @change="answerUpdate" :errors="errors"
              :default-value="application.answers"
              :readonly="!!userId" :show-errors="showErrors"
          />
        </div>

        <div class="text-center">
          <button id="kt_sign_up_submit" ref="submitButton" type="submit" class="btn-gradient w-full">
            {{ !!application ? 'Сохранить' : 'Отправить' }} заявку
          </button>
        </div>
      </div>
    </Form>
  </div>
</template>

<script setup>
import {computed, ref} from "vue"
import {Form} from "vee-validate"
import ProgressBar from "@/components/progressbar/ProgressBar.vue"
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


const props = defineProps(["game_alias", "userId"])
const questions = ref([])
const showErrors = ref(false)
const answers = ref({})
const application = ref({
  id: 1, status: "approved", answers: [], price: 0
})
const game_alias = props.game_alias
const user_id = computed(() => props.userId || store.getters['auth/user'].id)
gamesService.application(user_id.value, game_alias).then(({data}) => {
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
    gamesService.application(user_id.value, game_alias).then(({data}) => {
      application.value = data
    })
  })
}
</script>
