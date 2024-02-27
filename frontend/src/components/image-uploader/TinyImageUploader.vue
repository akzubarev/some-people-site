<template>
  <div
    :class="
      `
      TinyImageUploader
      ${icon ? 'TinyImageUploader_WithIcon' : ''}
      ${Boolean(image) ? 'TinyImageUploader_Loaded' : ''}
    `.trim()
    "
    @click="onClick"
  >
    <div class="TinyImageUploader-Placeholder"></div>
    <div class="TinyImageUploader-Icon"></div>
    <!-- <input class="TinyImageUploader-Input" type="file" @change="onUpload"> -->
    <div
      class="TinyImageUploader-Image"
      :style="image ? `background-image: url(${image})` : ''"
    />
    <Uploader
      v-model="show"
      ref="uploader"
      :width="300"
      :height="300"
      langType="ru"
      noSquare
      noRotate
      noCircle
      @crop-success="cropSuccess"
      img-format="png"
    ></Uploader>
  </div>
</template>

<script>
import Uploader from "vue-image-crop-upload"
export default {
  name: "TinyImageUploader",
  props: {
    icon: Boolean,
    image: String
  },
  components: {
    Uploader
  },
  data() {
    return {
      show: false
    }
  },
  methods: {
    cropSuccess(imgDataUrl) {
      // console.log(imgDataUrl);
      this.$emit("upload", imgDataUrl)
      this.$el.querySelector(
        ".TinyImageUploader-Image"
      ).style.backgroundImage = imgDataUrl
    },
    onClick() {
      this.show = true
      // this.$el.querySelector('.TinyImageUploader-Input').dispatchEvent(
      //   new MouseEvent('click')
      // );
    }
  }
  // methods: {
  //   onClick() {
  //     this.$el.querySelector('.TinyImageUploader-Input').dispatchEvent(
  //       new MouseEvent('click')
  //     );
  //   },
  //   onUpload() {
  //     const input = this.$el.querySelector('.TinyImageUploader-Input');

  //     if (input.files && input.files[0]) {
  //       const reader = new FileReader();

  //       reader.onload = (e) => {
  //         const imageData = e.target.result;
  //         this.$el.querySelector('.TinyImageUploader-Image').style.backgroundImage =
  //           'url(' + imageData + ')';

  //         this.$el.classList.add('TinyImageUploader_Loaded');

  //         this.$emit('upload', imageData);
  //       }

  //       reader.readAsDataURL(input.files[0]);
  //     }
  //   }
  // },
}
</script>
<style>
.vue-image-crop-upload .vicp-wrap .vicp-operate a {
  color: var(--kt-gray-100);
}
.vue-image-crop-upload .vicp-wrap {
  width: auto;
  max-width: 400px;
}
.vue-image-crop-upload .vicp-crop-left {
  width: 100%;
}
.vue-image-crop-upload .vicp-img-container {
  margin: auto;
}
.vue-image-crop-upload .vicp-range {
  margin-left: auto !important;
  margin-right: auto !important;
}
.vue-image-crop-upload
  .vicp-wrap
  .vicp-step2
  .vicp-crop
  .vicp-crop-left
  .vicp-range
  input[type="range"]::-webkit-slider-thumb {
  background-color: #61c091;
}
.vue-image-crop-upload
  .vicp-wrap
  .vicp-step2
  .vicp-crop
  .vicp-crop-left
  .vicp-range
  input[type="range"]::-moz-range-thumb {
  background-color: #61c091;
}
.vue-image-crop-upload
  .vicp-wrap
  .vicp-step2
  .vicp-crop
  .vicp-crop-left
  .vicp-range
  input[type="range"]::-ms-thumb {
  background-color: #61c091;
}
.vue-image-crop-upload
  .vicp-wrap
  .vicp-step2
  .vicp-crop
  .vicp-crop-left
  .vicp-range
  input[type="range"]::-webkit-slider-runnable-track {
  background-color: rgba(255, 167, 33, 0.3);
}
.vue-image-crop-upload
  .vicp-wrap
  .vicp-step2
  .vicp-crop
  .vicp-crop-left
  .vicp-range
  input[type="range"]::-moz-range-track {
  background-color: rgba(255, 167, 33, 0.3);
}
.vue-image-crop-upload
  .vicp-wrap
  .vicp-step2
  .vicp-crop
  .vicp-crop-left
  .vicp-range
  input[type="range"]::-ms-fill-lower {
  background-color: rgba(255, 167, 33, 0.3);
}
.vue-image-crop-upload
  .vicp-wrap
  .vicp-step2
  .vicp-crop
  .vicp-crop-left
  .vicp-range
  input[type="range"]::-ms-fill-upper {
  background-color: rgba(255, 167, 33, 0.15);
}
.vue-image-crop-upload
  .vicp-wrap
  .vicp-step2
  .vicp-crop
  .vicp-crop-left
  .vicp-range
  input[type="range"]:focus::-webkit-slider-runnable-track {
  background-color: rgba(255, 167, 33, 0.5);
}
.vue-image-crop-upload
  .vicp-wrap
  .vicp-step2
  .vicp-crop
  .vicp-crop-left
  .vicp-range
  input[type="range"]:focus::-moz-range-track {
  background-color: rgba(255, 167, 33, 0.5);
}
.vue-image-crop-upload
  .vicp-wrap
  .vicp-step2
  .vicp-crop
  .vicp-crop-left
  .vicp-range
  input[type="range"]:focus::-ms-fill-lower {
  background-color: rgba(255, 167, 33, 0.45);
}
.vue-image-crop-upload
  .vicp-wrap
  .vicp-step2
  .vicp-crop
  .vicp-crop-left
  .vicp-range
  input[type="range"]:focus::-ms-fill-upper {
  background-color: rgba(255, 167, 33, 0.25);
}
</style>
<style lang="sass">
@import './TinyImageUploader.sass'
</style>
