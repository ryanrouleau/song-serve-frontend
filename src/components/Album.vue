<template>
  <!--<img :src="this.details.art.large" />-->
  <div class="generic-card">
    <img :id="this.details.albumId" v-lazy="this.details.art.large" class="img" />
    <div :id="this.details.albumId" class="sub-card artist-info" :style="this.styleObject">
      <span class="card-label album-name">{{ this.details.albumName }}</span>
      <br />
      <span class="card-label artist-name">{{ this.details.albumArtist }}</span>
    </div>
  </div>
</template>

<script>
import bus from './bus.js';

export default {
  props: {
    details: { required: true }
  },
  mounted() {
    let darkMuted = this.details.artPalette.darkMuted;
    if (darkMuted !== 'undefined') {
      this.styleObject.background = `linear-gradient(transparent, rgb(${darkMuted}), rgb(${darkMuted})`;
    }
    else {
      this.styleObject.background = `linear-gradient(transparent, #212121, #212121)`;
    }
  },
  data() {
    return {
      styleObject: {
        background: 'transparent'
      }
    }
  },
  methods: {
    close() {
      bus.$emit('close-album-view');
    }
  },
  components: {
  }
}
</script>

<style lang="scss">
@import '../assets/css/vars.scss';

$card-detail-height: 66px;

.generic-card {
  width: 200px;
  height: calc(200px + #{$card-detail-height});
  transition: 0.2s ease;
  cursor: pointer;
  -webkit-transform-style: preserve-3d;
  -webkit-transform:translate3d(0,0,0);
  box-shadow: $menu-shadow;

  .img {
    opacity: 0.7;
    width: 200px;
    height: 200px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    transition: 0.2s ease;
    -webkit-backface-visibility: hidden;
    object-fit: cover;
  }

}
.generic-card:hover {
  box-shadow: 0px 0px 40px 0px rgba(0,0,0, 0.1), 0px 17px 25px 0px rgba(0,0,0, 0.2);
  transform: translateY(-5px);
  color: rgba(255,255,255,1);
  transform: scale(1.01) translateY(-5px);

  img {
    opacity: 1;
  }
  .sub-card {
    //opacity: 0.8;
  }
}
.art-container {
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
}
.sub-card {
  width: 100%;
  height: calc(#{$card-detail-height} + #{$card-detail-height};
  margin-top: -$card-detail-height;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
  padding-top: calc(#{$card-detail-height} + 10px);
  text-align: center;
  position: relative;
  z-index: 2;
  -webkit-backface-visibility: hidden;
  opacity: 0.7;
  transition: 0.2s ease;
}
.card-label {
  display: inline-block;
  width: 85%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  line-height: 18px;
}
.album-name {
  font-weight: 900;
  font-size: 14px;
}
.artist-name {
  font-size: 14px;
}
</style>
