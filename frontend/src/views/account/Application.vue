<template class="relative">
  <div v-if="!!application.status"
       class="flex flex-col gap-medium bg-bg-transparent-white overflow-y-auto no-scrollbar p-6">
    <div class="text-large text-content-secondary"> Заявка {{
        $t(`application.${application.status}`).toLowerCase()
      }}
    </div>
    <CharacterBlock v-if="!!application.character" :character="application.character" :game_alias="game_alias"
                    :personal="true"/>
    <div class="flex flex-row items-center gap-2 text-medium text-content-secondary">
      <inline-svg v-if="questionnaire_questions === questionnaire_answers"
                  class="w-6 h-6" :src="require('@/assets/images/icons/common/check.svg')"/>
      Опросник: {{ questionnaire_questions === questionnaire_answers ? "пройден" : "" }}
      <a v-if="questionnaire_questions != questionnaire_answers" class="underline"
         :href="`/account/${game_alias}/questionnaire`"> заполнить </a>
      <Undone v-if="questionnaire_questions != questionnaire_answers"
              :number="questionnaire_questions - questionnaire_answers"/>
    </div>
    <div class="text-medium text-content-secondary font-bold">
      <inline-svg v-if="application.price && application.payed == application.price"
                  class="w-6 h-6" :src="require('@/assets/images/icons/common/check.svg')"/>
      Взнос: {{ application.price ? `${application.payed} / ${application.price}` : 'не объявлен' }}
      <a v-if="application.price && application.payed != application.price" class="underline" href="/"> Оплатить </a>
    </div>
    <div class="flex flex-row items-center gap-2 text-medium text-content-secondary font-bold">
      <inline-svg v-if="questions.length == Object.values(answers).filter(a=>!!a).length"
                  class="w-6 h-6" :src="require('@/assets/images/icons/common/check.svg')"/>
      Дополнительная информация
      <Undone :number="questions.length - Object.values(answers).filter(a=>!!a).length"/>
    </div>
    <Form v-if="questions" class="form flex flex-col w-full gap-6" novalidate="novalidate" @submit="onSubmit">
      <QuestionField
          v-for="question in questions" :key="question"
          :question="question" :horizontal="false" :value="answers"
          @change="answerUpdate" :errors="errors"
          :default-value="application.answers"
      />
    </Form>
  </div>
  <Form v-else class="flex flex-col gap-medium bg-bg-transparent-white overflow-y-auto no-scrollbar p-6"
        novalidate="novalidate" @submit="onSubmit">
    <div class="text-large text-content-secondary"> Заявка не подана</div>
    <button ref="submitButton" type="submit" class="btn-gradient w-full text-center text-xl">
      Подать заявку
    </button>
  </Form>
</template>

<script setup lang="ts">
import {computed, ref} from "vue"
import {useStore} from "vuex"
import {useI18n} from "vue-i18n"
import CharacterBlock from "@/views/games/roles/groups/CharacterBlock.vue";
import gamesService from "@/services/gamesService";
import QuestionField from "@/views/account/questionnaire/QuestionField.vue";
import {Form} from "vee-validate";
import formhelper from "@/core/helpers/form"
import Undone from "@/views/account/drawer/Undone.vue";


const {t} = useI18n()
const store = useStore()
const user = computed(() => store.getters["auth/user"])
const user_id = store.getters['auth/user'].id

const props = defineProps(["game_alias"])
const game_alias = props.game_alias
const answers = ref({})
const questions = ref([])
const questionnaire_questions = ref(0)
const questionnaire_answers = ref(0)
const form = formhelper()
const {errors} = form
const application = ref({
  id: 1, status: null, answers: [], price: 0, payed: 0, character: {},
})


const loadData = () => {
  gamesService.application(user_id, game_alias).then(({data}) => {
    application.value = data
    if (!!data.answers) {
      gamesService.questions(game_alias).then(({data}) => {
        if (!!data) {
          questions.value = data.filter(q => q.order < 0)
          questionnaire_questions.value = data.filter(q => q.order > 0).length
          answers.value = Object.fromEntries(
              Object.entries(application.value.answers).filter((q_id, a) => questions.value.find(q => q.id == q_id)?.order < 0)
          )
          questionnaire_answers.value = Object.entries(application.value.answers).filter(
              (q_id, a) => !!a && questions.value.find(q => q.id == q_id)?.order > 0
          ).length
        }
      })
    }
  })
}

loadData()

const answerUpdate = (question, answer) => {
  answers.value[question] = answer
}

const onSubmit = (values) => {
  answers.value = {...values, ...answers.value, game_alias: game_alias}
  form.send(async () => {
    await gamesService.apply({game_alias: game_alias, ...answers.value})
    loadData()
  })
}
</script>
