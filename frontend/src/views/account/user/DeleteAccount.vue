<template>
  <!-- <div class="card mt-5">
    <div class="card-body">
      <Form class="form" novalidate="novalidate" @submit="deleteProfile">
        <Field
          name="current_password"
          class="form-control form-control-lg form-control-solid mb-3 mb-lg-0"
          :placeholder="$t('settings.currentPassword')"
          type="password"
        />
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <span>{{ errors.current_password || "" }}</span>
          </div>
        </div>
        <button class="btn btn-danger mt-3" type="submit">
          <span class="indicator-label">
            {{ $t("settings.deleteAccount") }}
          </span>
        </button>
      </Form>
    </div>
  </div> -->
</template>

<script setup>
  const deleteProfile = values => {
    Swal.fire({
      title: t("settings.deleteAccountApproveMessage"),
      showDenyButton: true,
      confirmButtonText: t("common.actions.cancel"),
      // showCancelButton: true,
      // confirmButtonText: 'Отменить',
      denyButtonText: t("common.actions.delete")
    }).then(result => {
      if (result.isDenied) {
        form.send(async () => {
          await authService.delete(store.getters["auth/user"].uuid, values)
          // successPopup('Аккаунт удален');
          window.location.reload()
        })
      }
    })
  }
</script>

