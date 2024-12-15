<template>
  <Form class="flex flex-col items-center gap-6 p-3 form w-full max-w-[500px]" @submit="onSubmitLogin">
    <InputField
        title="" :errors="errors.login_field || our_errors.login_field"
        name="login_field" type="email" :horizontal="true"
        :placeholder="$t('auth.loginField')" :autocomplete="true"

    />
    <InputField
        title="" :errors="errors.password || our_errors.password"
        name="password" :type="passVisible ? 'text' : 'password'" :horizontal="true"
        :placeholder="$t('common.password')" :autocomplete="true"
    >
      <!--      <router-link to="/lost-pass" class="link-primary"> {{ $t("auth.lostPassword") }}?</router-link>-->
    </InputField>
    <div class="flex flex-col w-full items-center gap-1">
      <router-link class="text-lg text-active-primary underline" to="/sign-up">
        {{ $t("auth.signUp") }}
      </router-link>
      <button class="btn-primary text-center w-full p-3" type="submit" ref="submitButton">
        {{ $t("auth.signIn") }}
      </button>
    </div>
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
const our_errors = ref({})
const onSubmitLogin = values => {
  store.dispatch("body/showActionLoader")
  our_errors.value = {}
  form.send(async () => {
    try {
      values.login_field = values.login_field.trim()
      values.email = values.login_field
      const data = (await authService.login(values))["data"]
      if (!Object.keys(errors.value).length) {
        await store.dispatch("auth/setToken", data.auth_token)
        await router.push("/")
      }
    } catch (Exception) {
      our_errors.value = {
        'login_field': 'Неверный логин или пароль',
        'password': 'Неверный логин или пароль',
      }
    }
    store.dispatch("body/hideActionLoader")
  })
}

</script>
