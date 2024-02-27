<template>
  <Dropdown>
    <template #button>
      <div class="CountrySwitcher-Switcher gap-2">
        <img
            v-if="active != 'AUTO'"
            class="rounded-full h-6 w-6 d-inline object-cover"
            :src="`https://flagcdn.com/h40/${active.toLowerCase()}.png`"
        />
        <img
            v-else
            class="rounded-full h-6 w-6"
            :src="require(`@/assets/images/countryswitcher/auto.svg`)"
        />
        <span v-if="withName" class="fs-5">
         {{
            countries[active] ? (autoCountry && active != 'AUTO' ? countries[active].name + " (Auto)" : countries[active].name) : "AUTO"
          }}
        </span>
      </div>
    </template>

    <ul class="max-h-[300px] min-w-[200px] overflow-auto">
      <Field
          type="text" name="countrySearch"
          class="form-control form-control-lg form-control-solid"
          :placeholder="$t('common.actions.search')"
          v-model="search"
      />
      <li v-for="(country, code) in filterCountries()"
          :key="code" @click="saveCountry(code)">
        <a
            class="flex items-center py-2 px-3 rounded-xl w-max max-w-[280px] break-words"
            :class="[active == code && 'bg-gray-800']" href="#">
          <img
              v-if="code != 'AUTO'"
              class="rounded-full h-6 w-6 d-inline object-cover"
              :src="`https://flagcdn.com/h40/${code.toLowerCase()}.png`"
          />
          <img
              v-else
              class="rounded-full h-6 w-6 d-inline"
              :src="require(`@/assets/images/countryswitcher/auto.svg`)"
          />
          <span class="ms-3 w-full">{{ country.name }}</span>
        </a>
      </li>
    </ul>
  </Dropdown>
</template>
<script>
import {ref} from "vue"
import {countries} from "@/components/countryswitcher/countries";
import Dropdown from '@/components/Dropdown'
import {Field} from "vee-validate";

export default {
  name: "country-switcher",
  props: {
    withName: Boolean,
    auto: Boolean,
    current: String,
  },
  components: {
    Field,
    Dropdown
  },
  emits: ['changedCountry'],
  setup(props, ctx) {
    const active = ref(props.current)
    const autoCountry = ref(props.auto)
    const search = ref("")
    const saveCountry = code => {
      active.value = code
      autoCountry.value = code === "AUTO"
      ctx.emit('changedCountry', code, countries[code]["name"])
    }
    const filterCountries = () => {
      // return countries.filter((country, code) => {
      //   return country.name.toLowerCase().includes(search.value.toLowerCase())
      // })
      const filteredCountries = {}
      for (const code in countries) {
        if (countries[code].name.toLowerCase().includes(search.value.toLowerCase()))
          filteredCountries[code] = countries[code]
      }
      return filteredCountries
    }
    return {
      countries: countries,
      search,
      filterCountries,
      active,
      autoCountry,
      saveCountry,
    }
  }
}
</script>
<style lang="scss">
.CountrySwitcher {
  &-Switcher {
    cursor: pointer;
    display: flex;
    align-items: center;
  }
}
</style>
