<template>
  <div
    class="flex flex-col flex-col-fluid bgi-position-y-bottom position-x-center bgi-no-repeat bgi-size-contain bgi-attachment-fixed"
    style="background-image: url('media/svg/illustrations/progress.svg')"
  >
    <!--begin::Content-->
    <div class="flex flex-col flex-col-fluid text-center p-10 py-lg-20">
      <!--begin::Logo-->
      <a href="#" class="mb-10 pt-lg-20">
        <img alt="Logo" src="media/logos/logo-2-dark.svg" class="h-50px mb-5" />
      </a>
      <!--end::Logo-->

      <!--begin::Wrapper-->
      <div class="pt-lg-10">
        <!--begin::Logo-->
        <h1 class=" fs-4x text-gray-700 mb-10">
          System Error
        </h1>
        <!--end::Logo-->

        <!--begin::Message-->
        <div class="fw-bold fs-3 text-gray-400 mb-15">
          Something went wrong! <br />
          Please try again later.
        </div>
        <!--end::Message-->

        <!--begin::Action-->
        <div class="text-center">
          <a href="#" class="btn btn-lg btn-primary "
            >Go to homepage</a
          >
        </div>
        <!--end::Action-->
      </div>
      <!--end::Wrapper-->
    </div>
    <!--end::Content-->

    <!--begin::Footer-->
    <div class="flex flex-center flex-col-auto p-10">
      <!--begin::Links-->
      <div class="flex items-center fw-bold fs-6">
        <a href="#" class="text-muted text-hover-primary px-2">About</a>

        <a href="#" class="text-muted text-hover-primary px-2">Contact</a>

        <a href="#" class="text-muted text-hover-primary px-2">Contact Us</a>
      </div>
      <!--end::Links-->
    </div>
    <!--end::Footer-->
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "error-500",
  components: {}
})
</script>
