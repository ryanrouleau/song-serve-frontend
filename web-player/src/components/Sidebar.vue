<template>
  <div id="sidebar">
    <transition name="fade">
      <div id="sidebar-disable-overlay" v-show="isDisabled"></div>
    </transition>
    <div id="logo">
      <h1 id="name">
        Song Serve
      </h1>
    </div>

    <sidebar-menu>

    </sidebar-menu>

  </div>
</template>

<script>
import SidebarMenu from './SidebarMenu.vue';
import SidebarMenuItem from './SidebarMenuItem.vue';
import bus from './bus.js';

export default {
  mounted() {
    bus.$on('disable-sidebar', this.disableSidebar);
    bus.$on('enable-sidebar', this.enableSidebar);
  },
  components: {
    SidebarMenu,
    SidebarMenuItem
  },
  data () {
    return {
      isDisabled: false
    }
  },
  methods: {
    disableSidebar() {
      this.isDisabled = true;
    },
    enableSidebar() {
      this.isDisabled = false;
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/css/vars.scss';

#sidebar {
  width: $sidebar-width;
  height: calc(100% - #{$player-height});
  overflow-y: auto;
  background: $grey;
  color: rgba(255,255,255,0.6);
  z-index: 1;
}

#logo {
  position: relative;
  padding: 27px 35px 0px 35px;
  font-weight: 900;
  z-index: 1;
  #name {
    font-size: 50px;
    font-weight: 900;
    color: rgba(255,255,255,0.8);
    //background: linear-gradient(60deg, #00A8C5, #FFFF7E);
    //-webkit-background-clip: text;
    //-webkit-text-fill-color: transparent;
  }
}

#sidebar-disable-overlay {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: $sidebar-width;
  z-index: 4;
  background: rgba(0,0,0,0.8);
}

.fade-enter-active, .fade-leave-active {
  transition: transform 0.2s ease, opacity 0.3s ease;
  //transform: translateX(0);
  opacity: 1;

}
.fade-enter, .fade-leave-to {
  //transform: translateX(-100%);
  opacity: 0;
}
</style>
