<template>
  <Form class="form w-full"
        novalidate="novalidate" @submit="onSubmitRegister">
    <div class="flex flex-col gap-3">
      <div class="grid gap-3 lg:grid-cols-2 flex-wrap">
        <div>
          <label class="form-label text-2xl">
            {{ $t("user.firstName") }}
          </label>
          <Field
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
                 autocomplete="off"/>
          <div class="fv-plugins-message-container">
            <div class="fv-help-block">
              <span>{{ errors.last_name || "" }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="fv-row">
        <Field class="form-control form-control-lg form-control-solid"
               type="text" placeholder="" name="username"
               autocomplete="off"/>
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <span>{{ errors.username || "" }}</span>
          </div>
        </div>
      </div>
      <div class="fv-row">
        <Field class="form-control form-control-lg form-control-solid"
               type="email" placeholder="" name="email"
               autocomplete="off"/>
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <span>{{ errors.email || "" }}</span>
          </div>
        </div>
      </div>
      <div class="fv-row gap-1" data-kt-password-meter="true">
        <label class="form-label text-2xl">
          {{ $t("common.password") }}
        </label>
        <Field class="form-control form-control-lg form-control-solid"
               type="password" placeholder=""
               name="password" autocomplete="off"/>
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <span>{{ errors.password || "" }}</span>
          </div>
        </div>
        <div class="fv-row gap-1">
          <label class="form-label text-2xl">{{
              $t("settings.repeatPassword")
            }}</label>
          <Field class="form-control form-control-lg form-control-solid"
                 type="password" placeholder=""
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
import {useStore} from "vuex"
import {useRouter} from "vue-router"
import authService from "@/services/authService"
import formhelper from "@/core/helpers/form"

export default defineComponent({
  name: "sign-up",
  components: {
    Field,
    Form,
  },
  setup() {
    const store = useStore()
    const router = useRouter()

    const country_iso = ref("AUTO")
    const country = ref("Auto")
    const submitButton = ref < HTMLElement | null > (null)
    const form = formhelper()
    const {errors} = form

    const onSubmitRegister = values => {
      form.send(async () => {
        values.email = (values.email || "").trim().toLowerCase()
        const data = (await authService.register(values))["data"]
        store.dispatch("auth/setToken", data.auth_token)
        router.push("/")
      })
    }

    return {
      errors,
      country_iso,
      country,
      onSubmitRegister,
      submitButton,
    }
  }
})
</script>
