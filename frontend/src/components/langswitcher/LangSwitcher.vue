<template>

  <Dropdown direction-y='toBottom'>
    <template #button>
      <div class="LangSwitcher-Switcher gap-2">
        <img
            class="rounded-full h-6 w-6 d-inline object-cover"
            :src="`https://flagcdn.com/h40/${langs[active].isoCode}.png`"
        />
        <span v-if="withTitle" class="fs-5">{{ langs[active].title }}</span>
      </div>
    </template>
    <ul class="min-w-[200px]">
      <li v-for="(lang, code) in langs" :key="code" @click="onChange(code)">
        <a :class="['flex items-center min-w-max w-full px-3 py-2 rounded-xl', active == code && 'bg-gray-800']"
           href="#">
          <img
              class="rounded-full h-6 w-6 d-inline object-cover"
              :src="`https://flagcdn.com/h40/${lang.isoCode}.png`"
          />
          <div class="ms-3">{{ lang.title }}</div>
        </a>
      </li>
    </ul>
  </Dropdown>
</template>
<script>
import {ref} from "vue"
// import i18n from "@/i18n";
import Cookies from "js-cookie"
import Dropdown from '@/components/Dropdown'
import {useStore} from "vuex";

export default {
  name: "lang-switcher",
  components: {
    Dropdown
  },
  props: {
    withTitle: Boolean
  },
  setup() {
    const langs = {
      en: {
        title: "English",
        isoCode: "gb"
      },
      ru: {
        title: "Русский",
        isoCode: "ru"
      },
      hu: {
        title: "Magyar",
        isoCode: "hu"
      },
      ro: {
        title: "Română",
        isoCode: "ro"
      },
      it: {
        title: "Italiano",
        isoCode: "it"
      },
      de: {
        title: "Deutsch",
        isoCode: "de"
      },
      uk: {
        title: "Українськa",
        isoCode: "ua"
      },
      fr: {
        title: "Français",
        isoCode: "fr"
      },
      cs: {
        title: "Czech",
        isoCode: "cz"
      },
      si: {
        title: "Slovenščina",
        isoCode: "si"
      },
      es: {
        title: "Español",
        isoCode: "es"
      },
      tr: {
        title: "Türkçe",
        isoCode: "tr"
      },
      pt: {
        title: "Português",
        isoCode: "pt"
      }
    }
    const store = useStore()
    const active = ref(store.getters['auth/user'].locale || "en")
    const onChange = code => {
      Cookies.set("django_language", code)
      store.getters['auth/user'].locale = code
      // active.value = code;
      window.location.reload()
    }
    return {
      langs,
      active,
      onChange
    }
  }
}
</script>
<style lang="scss">
.LangSwitcher {
  &-Switcher {
    cursor: pointer;
    display: flex;
    align-items: center;
  }
}
</style>
