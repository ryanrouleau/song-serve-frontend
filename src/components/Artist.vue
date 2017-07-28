<template>
  <!--<img :src="this.details.art.large" />-->
  <div class="generic-card">
    <img v-lazy="this.details.art.large" class="img" />
    <div :id="this.details.artistId" class="sub-card artist-info" :style="this.styleObject">
      <span class="card-label album-name">{{ this.details.artistName }}</span>
      <br />
    </div>
  </div>
</template>

<script>

export default {
  props: {
    details: { required: true }
  },
  mounted () {
    let darkMuted = this.details.artPalette.darkMuted;
    if (darkMuted !== 'undefined') {
      this.styleObject.background = `linear-gradient(transparent, rgb(${darkMuted}), rgb(${darkMuted})`;
    }
    else {
      this.styleObject.background = `linear-gradient(transparent, #212121, #212121)`;
    }
  },
  data () {
    return {
      styleObject: {
        background: 'transparent'
      }
    }
  },
  methods: {
  }
}
</script>

<style lang="scss" scoped>
.card-label {
  white-space: normal;
}

</style>
