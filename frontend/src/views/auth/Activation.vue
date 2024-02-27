<template>
  <!--begin::Wrapper-->
  <div class="w-lg-500px w-full rounded shadow-sm p-10 p-lg-15 mx-auto">
    <!--begin::Form-->
    <Form class="form w-full" id="kt_login_signin_form" @submit="onSubmitLogin">
      <!--begin::Heading-->
      <div class="text-center mb-10">
        <!--begin::Title-->
        <h1 class="text-dark mb-3">
          {{ $t("auth.approveEmail") }}
        </h1>
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
            {{ $t("common.actions.approve") }}
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
import { Form } from "vee-validate"
import { useRouter } from "vue-router"
import authService from "@/services/authService"
import formhelper from "@/core/helpers/form"

export default defineComponent({
  name: "activation",
  props: ["uid", "token"],
  components: {
    Form
  },
  setup(props) {
    const params = props
    const router = useRouter()
    const submitButton = ref<HTMLElement | null>(null)
    const form = formhelper()

    const { errors } = form

    const onSubmitLogin = () => {
      form.send(async () => {
        await authService.activate({
          uid: params["uid"],
          token: params["token"]
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
