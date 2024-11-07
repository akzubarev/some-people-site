<template>
  <Form class="flex flex-col gap-6 p-3 form w-full" @submit="onSubmitLogin">
    <InputField
        :title="$t('auth.loginField')" :errors="errors.login_field"
        name="login_field" type="email" :horizontal="true"
        placeholder="email"

    />
    <InputField
        :title="$t('common.password')" :errors="errors.password"
        name="password" :type="passVisible ? 'text' : 'password'" :horizontal="true"
        placeholder="Пароль"
    >
      <router-link to="/lost-pass" class="link-primary"> {{ $t("auth.lostPassword") }}?</router-link>
    </InputField>
    <button class="btn-gradient text-center w-full mt-3" type="submit" ref="submitButton">
      {{ $t("auth.signIn") }}
    </button>
  </Form>
</template>

<script lang="ts">
import {defineComponent, ref} from "vue"
import {Field, Form} from "vee-validate"
import {useStore} from "vuex"
import {useRouter, useRoute} from "vue-router"
// import { useI18n } from "vue-i18n";
import authService from "@/services/authService"
import formhelper from "@/core/helpers/form"
import InputField from "@/components/InputField.vue";

export default defineComponent({
  name: "sign-in",
  components: {
    InputField,
    Field,
    Form
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()
    // const { t } = useI18n();
    const submitButton = ref<HTMLElement | null>(null)
    const passVisible = ref<boolean>(false)
    const form = formhelper()

    const {errors} = form
    const onSubmitLogin = values => {
      form.send(async () => {
        values.login_field = values.login_field.trim()
        values.email = values.login_field
        const data = (await authService.login(values))["data"]
        store.dispatch("auth/setToken", data.auth_token)
        router.push("/")
      })
    }

    return {
      route,
      errors,
      onSubmitLogin,
      submitButton,
      passVisible
    }
  }
})
</script>
