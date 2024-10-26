<template>
  <!--begin::Form-->
  <Form class="form w-full" @submit="onSubmitLogin">
    <!--begin::Heading-->
    <div class="text-center mb-6">
      <!--begin::Title-->
      <!--      <h1 class="mb-3 text-3xl">-->
      <!--        {{ $t("auth.signIn") }}-->
      <!--      </h1>-->
      <!--end::Title-->
    </div>

    <!--begin::Input group-->
    <div class="mb-6">
      <!--begin::Label-->
      <label class="text-2xl">{{ $t("auth.loginField") }}</label>
      <!--end::Label-->

      <!--begin::Input-->
      <Field
          class="form-control form-control-lg form-control-solid"
          type="email" name="login_field" autocomplete="email"
      />
      <!--end::Input-->

      <div>
        <span>{{ errors.login_field || "" }}</span>
      </div>

    </div>
    <!--end::Input group-->

    <!--begin::Input group-->
    <div class="mb-6">
      <!--begin::Wrapper-->
      <div class="flex justify-between mb-2">
        <label class="text-2xl mb-0">{{ $t("common.password") }}</label>

        <!--begin::Link-->
        <router-link to="/lost-pass" class="link-primary">
          {{ $t("auth.lostPassword") }}?
        </router-link>
        <!--end::Link-->
      </div>
      <!--end::Wrapper-->

      <!--begin::Input-->
      <div class="flex relative">
        <Field
            class="form-control form-control-lg form-control-solid"
            :type="passVisible ? 'text' : 'password'"
            name="password"
            autocomplete="off"
        />
        <div
            @click="passVisible = !passVisible"
            class="absolute right-[1rem] my-auto top-[.75rem]"
            role="button">
          <inline-svg
              class="text-3xl text-gray-400"
              :src="require(`@/assets/images/icons/auth/eye${passVisible ? '-off' : ''}.svg`)"/>
        </div>
        <!--end::Input-->
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <span>{{ errors.password || "" }}</span>
          </div>
        </div>
      </div>
    </div>
    <!--end::Input group-->

    <!--begin::Actions-->
    <div class="text-center">
      <!--begin::Submit button-->
      <button type="submit" ref="submitButton"
              class="btn btn-lg btn-accent w-full">
        {{ $t("auth.signIn") }}
      </button>
      <!--end::Submit button-->
    </div>
    <!--begin::Link-->
<!--    <div class="text-gray-400 mt-3 text-center fs-4">-->
    <!--      {{ $t("auth.noAccount") }}-->

    <!--      <router-link-->
    <!--          :to="'/sign-up' + ((route.query.r && '?r=' + route.query.r) || '')"-->
    <!--          class="link-primary underline underline-offset-4"-->
    <!--      >-->
    <!--        {{ $t("auth.signUp") }}-->
    <!--      </router-link>-->
    <!--    </div>-->
    <!--end::Link-->
    <!--end::Actions-->
  </Form>
  <!--end::Form-->

</template>

<script lang="ts">
import {defineComponent, ref} from "vue"
import {Field, Form} from "vee-validate"
import {useStore} from "vuex"
import {useRouter, useRoute} from "vue-router"
// import { useI18n } from "vue-i18n";
import authService from "@/services/authService"
import formhelper from "@/core/helpers/form"

export default defineComponent({
  name: "sign-in",
  components: {
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
        values.login_field = values.login_field.trim().toLowerCase()
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
