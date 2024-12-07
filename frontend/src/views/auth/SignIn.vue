<template>
  <Form class="flex flex-col gap-6 p-3 form w-full" @submit="onSubmitLogin">
    <InputField
        :title="$t('auth.loginField')" :errors="errors.login_field"
        name="login_field" type="email" :horizontal="true"
        placeholder="email" :autocomplete="true"

    />
    <InputField
        :title="$t('common.password')" :errors="errors.password"
        name="password" :type="passVisible ? 'text' : 'password'" :horizontal="true"
        placeholder="Пароль" :autocomplete="true"
    >
      <router-link to="/lost-pass" class="link-primary"> {{ $t("auth.lostPassword") }}?</router-link>
    </InputField>
    <button class="btn-gradient text-center w-full mt-3" type="submit" ref="submitButton">
      {{ $t("auth.signIn") }}
    </button>
  </Form>
</template>

<script setup lang="ts">
import {ref} from "vue"
import {Form} from "vee-validate"
import {useStore} from "vuex"
import {useRouter, useRoute} from "vue-router"
import authService from "@/services/authService"
import formhelper from "@/core/helpers/form"
import InputField from "@/components/InputField.vue";

const store = useStore()
const router = useRouter()
const route = useRoute()
const submitButton = ref<HTMLElement | null>(null)
const passVisible = ref<boolean>(false)
const form = formhelper()

const {errors} = form
const onSubmitLogin = values => {
  form.send(async () => {
    values.login_field = values.login_field.trim()
    values.email = values.login_field
    const data = (await authService.login(values))["data"]
    if (!Object.keys(errors.value).length) {
      await store.dispatch("auth/setToken", data.auth_token)
      await router.push("/")
    }
  })
}

</script>
