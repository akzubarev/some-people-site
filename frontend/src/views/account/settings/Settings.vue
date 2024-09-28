<template>
  <div class="flex flex-col p-6 gap-6 rounded-xl bg-gray-700 bg-opacity-60 mt-48 mx-3">
    <MainSettings @saved="successPopup($t('common.actions.saved'))"/>
    <!--  <ActiveEmail @saved="successPopup($t('settings.emailWasSent'))" />-->
    <!--  <ChangeEmail-->
    <!--      @saved="successPopup($t('settings.emailChanged'))"-->
    <!--      @sent="successPopup($t('settings.emailWasSent'))"-->
    <!--      @error="errorPopup($t('settings.emailError'))"/>-->
    <ChangePassword
        @saved="successPopup($t('settings.passwordWasChanged'))"
        @error="errorPopup($t('settings.passwordDoesnotMatch'))"/>

    <div class="form flex flex-col gap-3">
      <button @click="$router.push('/sign-out')"
              class="btn btn-primary ml-auto w-fit max-sm:w-full">
        {{ $t("menu.logout") }}
      </button>
    </div>
  </div>
</template>


<script setup>
import MainSettings from "@/views/account/settings/MainSettings.vue"
// import ActiveEmail from "@/views/account/actions/ActiveEmail.vue"
// import ChangeEmail from "@/views/account/actions/ChangeEmail.vue"
import ChangePassword from "@/views/account/actions/ChangePassword.vue"


const successPopup = text => {
  setTimeout(() => {
    // Swal.fire({
    //   icon: "success",
    //   text: text
    // })
  }, 20)
}

const errorPopup = text => {
  setTimeout(() => {
    // Swal.fire({
    //   icon: "error",
    //   text: text
    // })
  }, 20)
}

</script>
