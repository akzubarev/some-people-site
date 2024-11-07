<template>
  <Form class="form w-full flex flex-col gap-6 p-3" novalidate="novalidate" @submit="onSubmitRegister">
    <div class="flex flex-row gap-3">
      <InputField
          :title="$t('user.firstName')" :errors="errors.first_name"
          name="first_name" placeholder="Имя" :horizontal="false"
      />
      <InputField
          :title="$t('user.lastName')" :errors="errors.first_name"
          name="last_name" placeholder="Фамилия" :horizontal="false"
      />
    </div>
    <div class="flex flex-row gap-3">
      <InputField
          :title="$t('user.username')" :errors="errors.username"
          name="username" :horizontal="false" :autocomplete="false"
      />
      <InputField
          :title="$t('user.email')" :errors="errors.email"
          name="email" type="email" placeholder="email" :horizontal="false"
      />
    </div>
    <div class="flex flex-row gap-3">
      <InputField
          :title="$t('common.password')" :errors="errors.password"
          name="password" type="password" placeholder="Пароль" :horizontal="false"
      />
      <InputField
          :title="$t('settings.repeatPassword')" :errors="errors.re_password"
          name="re_password" type="password" placeholder="Повторите пароль" :horizontal="false"
      />
    </div>
    <button id="kt_sign_up_submit" ref="submitButton" type="submit" class="btn-gradient w-full mt-3">
      <div class="indicator-label"> {{ $t("auth.signUp") }}</div>
      <div class="indicator-progress">
        <div class="spinner-border spinner-border-sm align-middle ms-2"></div>
      </div>
    </button>
  </Form>
</template>

<script>
import {defineComponent, ref, onMounted} from "vue"
import {Field, Form} from "vee-validate"
import {useStore} from "vuex"
import {useRouter} from "vue-router"
import authService from "@/services/authService"
import formhelper from "@/core/helpers/form"
import InputField from "@/components/InputField.vue";

export default defineComponent({
  name: "sign-up",
  components: {
    InputField,
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
        values.email = (values.email || "").trim()
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
