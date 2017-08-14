<template>
<div class="song" :style="this.styleObject">
  {{ index + 1 }}. {{ details.songName }} - <span style="font-size:14px; font-weight: 400">{{ details.artist }}</span>
</div>
</template>

<script>
export default {
  props: {
    details: { required: true },
    index: { required: true }
  },
  data () {
    return {
      styleObject: {
      }
    }
  },
  methods: {

  }
}
</script>

<style lang="scss">
@import '../assets/css/vars.scss';

.song {
  padding: 20px 20px;
  font-size: 18px;
  font-weight: 700;
  border-bottom: 1px solid rgba(0,0,0,0.15);
  border-top: 1px solid rgba(0,0,0,0.15);
  cursor: pointer;
  transition: 0.1s ease;
}
.song:hover {
  box-shadow: 0px 0px 51px 0px rgba(0, 0, 0, 0.1), 0px 0px 18px 0px rgba(0, 0, 0, 0.2);
}
</style>
