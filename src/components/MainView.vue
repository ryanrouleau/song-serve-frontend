<template>
  <div id="main-view">
    <albums-view v-show="(currentView === 'Albums')"></albums-view>
    <artists-view v-show="(currentView === 'Artists')"></artists-view>
  </div>
</template>

<script>
import AlbumsView from './AlbumsView.vue';
import ArtistsView from './ArtistsView.vue';
import * as Vibrant from 'node-vibrant';
import bus from './bus.js';

export default {
  mounted () {
    bus.$on('tab-changed', this.changeView);
  },
  methods: {
    changeView(newTab) {
      this.currentView = newTab;
      this.$Lazyload.lazyLoadHandler();
      this.$Lazyload.lazyLoadHandler();
    }
  },
  data () {
    return {
      currentView: 'Albums'
    }
  },
  components: {
    AlbumsView,
    ArtistsView,
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/css/vars.scss';

#main-view {
  width: calc(100% - #{$sidebar-width});
  height: 100%;
  position: absolute;
  right: 0;
  top: 0;
  background: $light-grey;
  z-index: 2;
  box-shadow: $menu-shadow;
}
</style>
