<template>
  <Popup @close="$emit('close')">
    <div
        class="flex flex-col gap-8 items-center text-white w-full lg:max-w-screen-md mx-auto p-5">
      <div class="flex flex-col gap-3 w-full">
        <span class="text-3xl">
          {{ $t("structure.newMailing") }}
        </span>
        <span class="text-gray-500">
          {{ $t("structure.forRecipients", {count: recipientsCount}) }}
        </span>
      </div>
      <div v-if="filters.length > 0" class="flex flex-col w-full gap-2">
        <div class="flex w-full gap-2 flex-wrap">
          <div
              v-for="filter, i in filters"
              :key="i"
              class="p-2 rounded-2xl bg-gray-800"
          >
            {{ filter }}
          </div>
        </div>
      </div>
      <div class="flex flex-col w-full gap-2">
        <div class="flex gap-8 w-full">
          <NormalImageUploader
              class="bg-gray-800 rounded-2xl w-full sm:w-80 !h-40 updoader-placeholder-icon"
              icon :image="image"
              @upload="image = $event"
          />
        </div>
      </div>

      <div class="flex flex-col gap-2 w-full">
        <label class="fw-bold fs-6">
          {{ $t("common.title") }}
        </label>
        <input type="text" v-model="title"
               class="form-control form-control-md px-15 bg-gray-800 border-0 text-white"
               name="search"
               :placeholder="$t('common.input') + '...'"/>
      </div>
      <div class="flex w-full flex-col gap-2 EditorTheme">
        <label class="fw-bold fs-6">
          {{ $t("common.message") }}
        </label>
        <QuillEditor
            v-model:content="text"
            contentType="html"
            :toolbar="['bold', 'italic', 'code', 'underline', 'strike']"
            :placeholder="$t('common.input') + '...'"
        />
      </div>

      <div class="flex w-full">
        <button class="btn btn-accent h-fit w-full md:w-fit" @click="send">
          {{ $t(`common.actions.send`) }}
        </button>
      </div>
    </div>
  </Popup>
</template>

<!-- @apply flex stroke-white #{!important}; -->
<style lang="scss">
.updoader-placeholder-icon {
  & .NormalImageUploader-Icon {
    @apply h-20
  }
}

.EditorTheme {
  @apply overflow-hidden;
  & .ql-snow {
    @apply border-0;
    &.ql-toolbar {
    }

    &.ql-container {
      @apply rounded-2xl bg-gray-800 font-['SuisseSign'];
      & .ql-editor {
        @apply min-h-[150px] text-lg;
        &::before {
          @apply text-[--kt-input-color] not-italic text-lg;
        }
      }
    }
  }

}
</style>

<script setup>
import {ref, onMounted} from "vue"
import {useI18n} from 'vue-i18n'
import {useRoute} from 'vue-router'
import Swal from "sweetalert2"
import notificationService from "@/services/notificationService"
import NormalImageUploader
  from "@/components/image-uploader/NormalImageUploader"
import {QuillEditor} from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css';
import Popup from '@/components/Popup'


const route = useRoute()
const t = useI18n().t;
const image = ref(null)
const text = ref("")
const title = ref("")
const filters = ref([])

const props = defineProps(['recipientsCount', 'usedFilters', 'search'])
const emit = defineEmits('close', 'success')

console.log(props.usedFilters)
const availableFilters = {
  targetMissions: m => m.sort().map(v => v > 3 ? `${v - 3} Energy` : `${v + 1} Camp`),
  onlyActive: v => v !== null ? (
      `${t('matrix.tree.missions')}: ${v === true ? t('matrix.tree.activated') : t('matrix.tree.notActivated')}`
  ) : [],
  onlySubscribed: v => v !== null ? (
      `${t('user.subscription')}: ${v === true ? t('user.active') : t('user.notActive')}`
  ) : [],
  search: v => v ? `🔍 ${v}` : []
}

const send = async () => {
  await notificationService.sendMailing({
    search: props.search,
    filters: props.usedFilters && JSON.parse(props.usedFilters),
    image: image.value,
    text: `<b>${title.value}</b>\n\n${text.value}`
  })
  emit('success')
}

onMounted(() => {
  filters.value = props.usedFilters ? Object.entries(Object.assign({search: props.search}, JSON.parse(props.usedFilters))).map(
      ([k, v]) => Object.keys(availableFilters).includes(k) ? availableFilters[k](v) : []
  ).flat() : []
})
</script>
