<template>
  <ProgressBar
      :class="progress.length ? 'h-[8px]' : '!h-0'"
      class="fixed top-0 rounded-0"
      color="linear-gradient(to right, #00c853, #004bff)"
      :progress="progress.length * 100 / 7"
  />
  <Form class="form w-full"
        novalidate="novalidate" @submit="onSubmitRegister">
    <div class="mb-10 text-center">

    </div>
    <div class="flex flex-col">
      <div class="grid gap-3 lg:grid-cols-2 flex-wrap mb-7">
        <div>
          <label class="form-label   text-2xl">
            {{ $t("user.firstName") }}
          </label>
          <Field
              @input="updateProgress"
              class="form-control form-control-lg form-control-solid"
              type="text" placeholder="" name="first_name"
              autocomplete="off"/>
          <div>
            <span>{{ errors.first_name || "" }}</span>
          </div>
        </div>
        <div>
          <label class="form-label   text-2xl">{{
              $t("user.lastName")
            }}</label>
          <Field class="form-control form-control-lg form-control-solid"
                 type="text" placeholder="" name="last_name"
                 @input="updateProgress"
                 autocomplete="off"/>
          <div class="fv-plugins-message-container">
            <div class="fv-help-block">
              <span>{{ errors.last_name || "" }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="fv-row mb-7">
        <div class="flex gap-2 items-center">
          <label class="form-label text-2xl">Email</label>
          <div role="button" data-bs-toggle="tooltip"
               data-bs-placement="right" data-bs-trigger="hover"
               class="h-fit pb-3" :title="$t('auth.emailHelp')">
            <inline-svg
                :src="require('@/assets/images/icons/matrix/Info.svg')"
                style="color: var(--kt-primary)">
            </inline-svg>
          </div>
        </div>
        <Field class="form-control form-control-lg form-control-solid"
               type="email" placeholder="" name="email"
               @input="updateProgress"
               autocomplete="off"/>
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <span>{{ errors.email || "" }}</span>
          </div>
        </div>
      </div>
      <div class="mb-10 fv-row" data-kt-password-meter="true">
        <div class="mb-1">
          <label class="form-label   text-2xl">
            {{ $t("common.password") }}
          </label>
          <div class="relative mb-3">
            <Field class="form-control form-control-lg form-control-solid"
                   type="password" placeholder=""
                   @input="updateProgress"
                   name="password" autocomplete="off"/>
            <div class="fv-plugins-message-container">
              <div class="fv-help-block">
                <span>{{ errors.password || "" }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="">
          <label class="form-label   text-2xl">{{
              $t("settings.repeatPassword")
            }}</label>
          <Field class="form-control form-control-lg form-control-solid"
                 type="password" placeholder=""
                 @input="updateProgress"
                 name="re_password" autocomplete="off"/>
          <div class="fv-plugins-message-container">
            <div class="fv-help-block">
              <span>{{ errors.re_password || "" }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="text-center">
        <button id="kt_sign_up_submit" ref="submitButton" type="submit"
                class="btn btn-lg btn-accent w-full">
            <span class="indicator-label">
              {{ $t("auth.signUp") }}
            </span>
          <span class="indicator-progress">
              <span
                  class="spinner-border spinner-border-sm align-middle ms-2"></span>
            </span>
        </button>
      </div>
    </div>
  </Form>
</template>

<script>
import {defineComponent, ref, onMounted} from "vue"
import {Field, Form} from "vee-validate"
import Cookies from "js-cookie"
import ProgressBar from "@/components/progressbar"
import {useStore} from "vuex"
import {useRouter} from "vue-router"
import authService from "@/services/authService"
import formhelper from "@/core/helpers/form"
import {Tooltip} from "bootstrap"

export default defineComponent({
  name: "sign-up",
  components: {
    Field,
    Form,
    ProgressBar,
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const progress = ref([])

    const updateProgress = event => {
      if (event.target.value && !progress.value.includes(event.target.name)) {
        progress.value.push(event.target.name)
      } else if (!event.target.value && progress.value.includes(event.target.name)) {
        progress.value.splice(progress.value.indexOf(event.target.name), 1)
      }
    }

    const country_iso = ref("AUTO")
    const country = ref("Auto")
    const submitButton = ref < HTMLElement | null > (null)
    const form = formhelper()
    const {errors} = form

    onMounted(() => {
      const tooltipTriggerList = [].slice.call(
          document.querySelectorAll('[data-bs-toggle="tooltip"]')
      )
      tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new Tooltip(tooltipTriggerEl)
      })
    })
    const onSubmitRegister = values => {
      // Clear existing errors
      // submitButton.value?.setAttribute("data-kt-indicator", "on");
      form.send(async () => {
        values.refer = 1
        values.email = (values.email || "").trim().toLowerCase()
        const data = (await authService.register(values))["data"]
        store.dispatch("auth/setToken", data.auth_token)
        router.push("/tariffs")
      })
    }

    return {
      errors,
      country_iso,
      country,
      onSubmitRegister,
      submitButton,
      progress,
      updateProgress
    }
  }
})
</script>
