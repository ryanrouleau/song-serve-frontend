<template>
<div class="popup" :style="this.styleObject">
  <div class="popup-overlay" :style="this.overlayStyleObject">
      <div class="popup-footer" :style="this.footerStyleObject">
        <span class="popup-album-name">{{ this.details.albumName }}</span>
        <span class="popup-album-artist-name">{{ this.details.albumArtist }}</span>
      </div>
      <div class="popup-footer-overlay"></div>
      <div class="popup-header">
        <div class="close" @click="close"><-</div>
      </div>
      <div class="song-container" :style="this.songContainerStyleObject">
        <song v-for="(song, index) in this.songs" :key="song.songId" :index="index" :details="song" @click.native="playSong(song)"></song>
      </div>
  </div>
</div>
</template>

<script>
import Song from './Song.vue';
import axios from 'axios';
import bus from './bus.js';

export default {
  props: {
    details: { required: true }
  },
  mounted () {
    console.log(this.details);
    //let popupWidth = 500;
    //let popupHeight = 600;
    //this.positionPopup(popupWidth, popupHeight);

    axios.get(`http://localhost:3000/api/album/${this.details.albumId}`).then(res => {
      this.songs = res.data.songs;
    })
    .catch(err => {
      alert(`Fatal error: ${err}`);
    });

  },
  data () {
    return {
      songs: [],
      styleObject: {
        background: `url(${this.details.art.mega})`
        //border: `4px solid rgb(${this.details.artPalette.darkMuted})s`
      },
      overlayStyleObject: {
        //background: `linear-gradient(rgba(${this.details.artPalette.darkVibrant}, 1), rgba(${this.details.artPalette.darkMuted}, 0))`,
        background: `linear-gradient(rgba(${this.details.artPalette.darkMuted},0), rgba(${this.details.artPalette.darkMuted},1))`
      },
      songContainerStyleObject: {
        //background: `rgb(${this.details.artPalette.darkMuted})`
        background: '#eaeaea'
      },
      footerStyleObject: {
        background: `rgb(${this.details.artPalette.darkMuted})`,
        color: `rgb(${this.details.artPalette.lightVibrant})`
      }
    }
  },
  methods: {
    playSong (song) {
      song.albumData = this.details;
      song.queue = this.songs;
      console.log(song);
      bus.$emit('play-song', song);
    },
    positionPopup (popupWidth, popupHeight) {
      let sidebarWidth = 240;
    },
    close () {
      bus.$emit('close-album-view');
    }
  },
  components: {
    Song
  }
}
</script>

<style lang="scss">
@import '../assets/css/vars.scss';

.popup {
  position: absolute;
  width: 600px;
  height: 600px;
  //height: calc(90% - #{$player-height});
  top: calc(50% - 300px - #{$player-height});
  left: calc(50% - 300px);
  z-index: 10;
  box-shadow: 0px 0px 51px 0px rgba(0, 0, 0, 0.2), 0px 6px 18px 0px rgba(0, 0, 0, 0.4);
  border-radius: 6px;
  overflow: hidden;
  background-size: cover !important;
  background-position: center center !important;
}
.popup-overlay {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  //background: rgba(33,33,33,0);
  border-radius: 5px;
  overflow: auto;
  border-radius: 5px;
}
.popup-footer {
  position: fixed;
  width: 600px;
  height: 80px;
  bottom: calc(50% - 265px);
  left: calc(50% - 300px + #{$sidebar-width}/2);
  //margin-left: calc(-350px + #{$sidebar-width}/2);
  z-index: 9;
  border-bottom-right-radius: 5px;
  border-bottom-left-radius: 5px;
  text-align: center;
  box-shadow: $menu-shadow;
}
.popup-footer-overlay {
  position: fixed;
  width: 600px;
  height: 75px;
  bottom: calc(50% - 260px);
  left: calc(50% - 300px + #{$sidebar-width}/2);
  background: rgba(255,255,255,0.06);
  z-index: 10;
}
.popup-album-name {
  display: inline-block;
  width: 100%;
  font-size: 24px;
  font-weight: 900;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  margin-top: 10px;
  margin-bottom: 0px;
}
.popup-album-artist-name {
  display: inline-block;
  width: 100%;
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.song-container {
  margin: 40% 50px 50px 50px;
  width: calc(100% - 100px);
  color: #212121;
  box-shadow: 0px 0px 51px 0px rgba(0, 0, 0, 0.2), 0px 0px 18px 0px rgba(0, 0, 0, 0.4);
  border-radius: 5px;
  //background: #f2f2f2;
  position: relative;
  z-index: 2;
}
.song-container .song:last-child {
  border-bottom: 0px;
}
.close {
  transform: translate(-223px, -19px) scale(1.5);
  cursor: pointer;
  opacity: 0.8;
  transition: 0.1s ease;
}
.close:hover {
  opacity: 1;
}
</style>
