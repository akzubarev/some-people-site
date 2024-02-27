<template>
  <div class="card">
    <div class="card-header !pb-0">
      <div class="card-title">
        {{ $t("common.settings") }}
      </div>
    </div>
    <div class="px-6">
      <div class="flex overflow-auto h-55px">
        <ul
            class="nav nav-stretch nav-line-tabs nav-line-tabs-2x border-transparent fs-5  flex-nowrap"
        >
          <li class="nav-item">
            <router-link
                to="/account/settings"
                class="nav-link text-active-primary me-6"
                active-class="active"
            >
              {{ $t("settings.common") }}
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
                to="/account/telegram"
                class="nav-link text-active-primary me-6"
                active-class="active"
            >
              Telegram
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
                to="/account/notifications"
                class="nav-link text-active-primary me-6"
                active-class="active"
            >
              {{ $t("menu.notifications") }}
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <router-view></router-view>
</template>

<script setup lang="ts">

</script>
