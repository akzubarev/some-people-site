<template>
  <div :class="['Tree-Item', matrix.virtual && 'Tree-Item_Virtual']">
    <!-- $store.getters['auth/user'].id==(matrix.user&&matrix.user.id)&&'Tree-Item_Me' -->
    <Avatar
      backgroundColor="#3150f6"
      v-if="!matrix.virtual && matrix.user && matrix.user.uuid"
      :src="matrix.user.avatar"
      @click="openStructure"
      :class="[
        'Tree-Avatar cursor-pointer',
        matrix.virtual && 'Tree-Avatar_Virtual'
      ]"
      :username="
        `${matrix.user.first_name || 'Н'} ${matrix.user.last_name || 'Д'}`
      "
      rounded
    />
    <Avatar
      v-else-if="!matrix.virtual"
      backgroundColor="#17233B"
      :color="
        matrix.index === undefined && !canbook && '#777'
      "
      :class="['Tree-Avatar',  canbook && 'cursor-pointer']"
      @click="book()"
      :username="matrix.index !== undefined ? matrix.index + 1 : '+'"
      rounded
    />
    <Avatar
      v-else
      :class="['Tree-Avatar', matrix.virtual && 'Tree-Avatar_Virtual']"
      :icon="`
        <svg width='17' height='16' viewbox='0 0 17 16' fill='none' xmlns='http://www.w3.org/2000/svg'>
          <path d='M13.333 5L7.61585 10.7172C7.45964 10.8734 7.20637 10.8734 7.05017 10.7172L4.33301 8' stroke='#000' stroke-width='1.5' stroke-linecap='round'/>
        </svg>
      `"
      backgroundColor="var(--kt-primary)"
      rounded
    />
    <div
      class="w-full text-center flex justify-center mt-2 cursor-pointer px-1"
      style="min-height: 20px;"
    >
      <div
        @click="openPopup"
        class="w-full flex items-center justify-center"
        v-if="!matrix.virtual && matrix.user && matrix.user.uuid"
      >
        <span class="Tree-Username">{{ matrix.user.username }}</span
        >&nbsp;
        <span v-if="matrix.gl">GL&nbsp;</span>
        <span v-if="matrix.structure_count" class="text-gray-400">
          {{ matrix.structure_count }}
        </span>
      </div>
      <!-- <span class="badge badge-pink text-black" v-if="matrix.virtual">↑</span> -->
      <span
        class="flex gap-1 flex-wrap justify-center"
        @click="$emit('deleteBooking', matrix.uuid)"
        v-if="!matrix.user && matrix.uuid"
      >

      	<div class="flex gap-1 flex-wrap justify-center max-w-[50px] sm:max-w-none">
          <span class="text-white"> {{ $t('matrix.tree.booking') }} </span>
      	  <span class="text-muted"> {{ matrix.uuid.split("-")[0] }} </span>
      	</div>
        <div class="flex absolute p-1 rounded-full bg-gray-300 items-center justify-center text-white"
          style="top: 0; z-index: 9; left: calc(50% + 12px); width: 22px; height: 22px">
          <div
            class="flex"
            style="height: min-content; z-index: 10; color: var(--kt-primary-inverse)"
            v-html="require('!!raw-loader!@/assets/images/icons/delete.svg').default"
            />
        </div>

      </span>
      <span
	     v-else-if="(!matrix.user || Object.keys(matrix.user).length === 0) && matrix.index === undefined"
	     :class="canbook ? 'text-white' : 'text-muted'"> {{ canbook ? $t('common.actions.book') : $t('matrix.tree.cantBook') }} </span>
      <span v-if="matrix.virtual" class="">{{ $t('matrix.tree.newClone') }}</span>

      <!-- <span class="badge badge-light-primary" @click="openPopup" v-if="!matrix.user&&matrix.uuid">Book</span> -->
    </div>
  </div>
</template>
<script>
// import { computed } from 'vue';
import Avatar from "@/components/avatar"
export default {
  name: "tree-item",
  components: {
    Avatar
  },
  emits: ["popup", "structure"],
  props: {
    matrix: {
      type: Object,
      default: () => ({ user: {} })
    },
    canbook: Boolean
  },
  setup(props, { emit }) {
    const openPopup = () => {
      emit("popup", props.matrix)
    }
    const openStructure = () => {
      emit("structure", props.matrix)
    }
    const book = () => {
      if (props.matrix.index === undefined && props.canbook) {
        emit("book")
      }
    }
    return {
      book,
      openPopup,
      openStructure
    }
  }
}
</script>
