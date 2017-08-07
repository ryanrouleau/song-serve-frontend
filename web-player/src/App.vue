<template>
  <div id="app">
    <sidebar></sidebar>
    <main-view></main-view>
    <transition name="slide-up">
      <player v-if="songPlaying" :details="this.songData">sdfsdfsd</player>
    </transition>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue';
import MainView from './components/MainView.vue';
import Player from './components/Player.vue';
import bus from './components/bus.js';

export default {
  name: 'app',

  mounted() {
    bus.$on('play-song', this.playSong);
    bus.$on('next-song', this.nextSong);
    bus.$on('prev-song', this.prevSong);
    this.queue = [];
    this.currentQueueIndex = 0;
  },
  components: {
    Sidebar,
    MainView,
    Player
  },
  methods: {
    playSong (song) {
      this.songData = song;
      this.queue = song.queue;
      this.currentQueueIndex = this.queue.findIndex(queueSong => {
        return song.songId === queueSong.songId;
      });
      this.songPlaying = true;
    },
    nextSong() {
      if (this.currentQueueIndex + 1 === this.queue.length) {
        this.currentQueueIndex = 0;
      }
      else this.currentQueueIndex++;
      this.songData = this.queue[this.currentQueueIndex];
    },
    prevSong() {
      if (this.currentQueueIndex - 1 === -1) {
        this.currentQueueIndex = this.queue.length-1;
      }
      else this.currentQueueIndex--;
      this.songData = this.queue[this.currentQueueIndex];
    }
  },
  data () {
    return {
      songPlaying: false,
      songData: {}
    }
  }
}
</script>

<style lang="scss">

#app {
  height: 100%;
  width: 100%;
}

.slide-up-enter-active, .slide-up-leave-active {
  transition: transform 0.4s ease;
  transform: translateY(0px);
}
.slide-up-enter, .slide-up-leave-to {
  transform: translateY(100px);
}
</style>
