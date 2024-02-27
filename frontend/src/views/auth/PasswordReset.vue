<template>
  <!--begin::Wrapper-->
  <div class="w-lg-500px w-full  rounded shadow-sm p-10 p-lg-15 mx-auto">
    <!--begin::Form-->
    <Form class="form w-full" id="kt_login_signin_form" @submit="onSubmitLogin">
      <!--begin::Input group-->
      <div class="fv-row mb-10">
        <!--begin::Input-->
        <label class="form-label fs-6  text-dark">{{
          $t("common.password")
        }}</label>
        <Field
          class="form-control form-control-lg form-control-solid"
          type="password"
          name="new_password"
          :placeholder="$t('settings.enterNewPassword')"
          autocomplete="off"
        />
        <!--end::Input-->
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <span>{{ errors.new_password || "" }}</span>
          </div>
        </div>
      </div>
      <!--end::Input group-->

      <!--begin::Actions-->
      <div class="text-center">
        <!--begin::Submit button-->
        <button
          type="submit"
          ref="submitButton"
          id="kt_sign_in_submit"
          class="btn btn-lg btn-primary w-full mb-5"
        >
          <span class="indicator-label">
            {{ $t("auth.signIn") }}
          </span>
        </button>
        <!--end::Submit button-->
      </div>
      <!--end::Actions-->
    </Form>
    <!--end::Form-->
  </div>
  <!--end::Wrapper-->
</template>

<script lang="ts">
import { defineComponent, ref } from "vue"
import { Field, Form } from "vee-validate"
import { useRouter } from "vue-router"
// import Swal from "sweetalert2/dist/sweetalert2.min.js";

import authService from "@/services/authService"
import formhelper from "@/core/helpers/form"

export default defineComponent({
  name: "password-reset",
  props: ["uid", "token"],
  components: {
    Field,
    Form
  },
  setup(props) {
    const router = useRouter()

    const submitButton = ref<HTMLElement | null>(null)
    const form = formhelper()

    const { errors } = form

    const params = props

    const onSubmitLogin = values => {
      // Clear existing errors
      // submitButton.value?.setAttribute("data-kt-indicator", "on");
      form.send(async () => {
        // const data = (await authService.login(values))["data"];

        await authService.passReset({
          uid: params["uid"],
          token: params["token"],
          /* @ts-ignore */
          new_password: values["new_password"]
        })

        router.push("/")
      })
    }

    return {
      errors,
      onSubmitLogin,
      submitButton
    }
  }
})
</script>
