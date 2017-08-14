<template>
  <div class="main-view">
    <transition name="fade">
      <div class="disable-view-overlay" v-show="isDisabled" @click="closeAlbumView"></div>
    </transition>
    <div class="main-view-header">
      <h1 class="main-view-title">Albums</h1>
      <div class="num-albums">Dispalying <span class="bold">{{ numberOfAlbums }}</span> albums</div>
    </div>
    <!--
    @click.native="openAlbumView(album)"
  -->
    <div class="grid" id="album-grid">
      <album v-for="album in this.albums" :key="album.albumId" @click.native="openAlbumView(album, $event)" :details="album"></album>
    </div>
    <div class="album-view-container">
      <transition name="fade">
        <album-view v-for="album in this.albums" :key="album.albumId" v-if="currentAlbumView === album.albumId" :details="album" @blur.native="closeAlbumView"></album-view>
      </transition>
    </div>
  </div>
</template>

<script>
import Album from './Album.vue';
import AlbumView from './AlbumView.vue';
import bus from './bus.js';
import axios from 'axios';

export default {
  created () {
    this.albums = [];
    this.getAlbums();
  },
  mounted() {
    bus.$on('close-album-view', this.closeAlbumView);
    bus.$on('album-clicked', this.openAlbum);
  },
  data () {
    return {
      numberOfAlbums: 0,
      currentAlbumView: 0,
      isDisabled: false,
    }
  },
  methods: {
    getAlbums () {
      axios.get('http://localhost:3000/api/albums').then(res => {
        res.data.albums.forEach(album => {
          if (album.art.small !== 'undefined') this.albums.push(album);
        })
        this.numberOfAlbums = this.albums.length;
        //this.numberOfAlbums = res.data.numberOfAlbums;
      })
      .catch(err => {
        alert(err);
      });
    },
    openAlbumView (data, e) {
      this.currentAlbumView = data.albumId;
      this.isDisabled = true;
      //bus.$emit('disable-sidebar');
      data.e = e;
      data.parentWidth = this.$el.clientWidth;
      data.parentHeight = this.$el.clientHeight;
    },
    closeAlbumView () {
      this.currentAlbumView = -1;
      this.isDisabled = false;
      //bus.$emit('enable-sidebar');
    }
  },
  components: {
    Album,
    AlbumView
  }
}
</script>

<style lang="scss">
@import '../assets/css/vars.scss';

.disable-view-overlay {
  position: absolute;
  top: 0;
  left: -$sidebar-width;
  z-index: 6;
  width: calc(100% + #{$sidebar-width};
  height: 100%;
  background: rgba(0,0,0,0.4);
}

.main-view-header {
  position: absolute;
  height: $header-height;
  width: calc(100%);
  background: linear-gradient(rgba(33,33,33,0.9), rgba(33,33,33,1));
  box-shadow: 0px 0px 51px 0px rgba(0, 0, 0, 0.1), 0px 6px 18px 0px rgba(0, 0, 0, 0.2);
  z-index: 5;
  color: $off-white;
}
.main-view-header::after {
  content: '';
  margin-top: -70px;
  height: 85px;
  width: 100%;
  background: rgba(255,255,255,0.01);
  z-index: 100;
  position: absolute;
}
.main-view-title {
  font-size: 24px;
  font-weight: 900;
  margin-top: 14px;
  text-transform: uppercase;
  text-align: center;

  .num-albums {
    font-weight: 400;
    font-size: 18px;
    display: block;
    transform: translate(0px, 2px);
    opacity: 0.7;
    float: right;
    padding-right: 20px;
    text-transform: none;
    text-align: center;
    width: 100%;
  }
}
.num-albums {
  font-size: 14px;
  text-align: center;
  margin-top: 6px;
}
.main-view {
  height: 100%;
  width: 100%;
}
.grid {
  max-height: 100%;
  padding: 40px;
  padding-top: calc(#{$header-height} + 35px);
  padding-right: 0px;
  display: grid;
  grid-gap: 40px;
  grid-template-columns: repeat(auto-fit, 200px);
  overflow-y: auto;
}

.scale-enter-active, .scale-leave-active {
  transition: transform 0.1s ease;
  transform: scale(100%, 100%);
}
.scale-enter, .scale-leave-to {
  transform: scale(0);
}

.fade-enter-active, .fade-leave-active {
  transition: transform 0.2s ease, opacity 0.3s ease;
  opacity: 1;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
