<template>
  <div
    class="flex flex-col flex-col-fluid bgi-position-y-bottom position-x-center bgi-no-repeat bgi-size-contain bgi-attachment-fixed"
    style="background-image: url('media/svg/illustrations/progress.svg')"
  >
    <!--begin::Content-->
    <div class="flex flex-col flex-col-fluid text-center p-10 py-lg-20">
      <!--begin::Logo-->
      <!--       <a href="#" class="mb-10 pt-lg-20">
        <img alt="Logo" src="media/logos/logo-2-dark.svg" class="h-50px mb-5" />
      </a> -->
      <!--end::Logo-->

      <!--begin::Wrapper-->
      <div class="pt-lg-10">
        <!--begin::Logo-->
        <h1 class=" fs-4x text-gray-700 mb-10">
          Страница не найдена
        </h1>
        <!--end::Logo-->

        <!--begin::Message-->
        <!--   <div class="fw-bold fs-3 text-gray-400 mb-15">
          The page you looked not found! <br />
          Plan your blog post by choosing a topic
        </div> -->
        <!--end::Message-->

        <!--begin::Action-->
        <div class="text-center">
          <a href="/" class="btn btn-lg btn-primary "
            >Перейти на главную</a
          >
        </div>
        <!--end::Action-->
      </div>
      <!--end::Wrapper-->
    </div>
    <!--end::Content-->
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "error-404",
  components: {}
})
</script>
