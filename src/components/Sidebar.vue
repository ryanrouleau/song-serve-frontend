<template>
  <div id="sidebar">

    <div id="logo">
      <h1 id="name">
        Song Serve
      </h1>
      <h1 id="ui">
        UI
      </h1>
    </div>

    <sidebar-menu>
      <div class="highlight-on-hover">
        <div class="seperator"></div>
        <h2>MANAGE</h2>
        <sidebar-menu-item v-for="item in this.libItems" :key="name" :name="item" @click="selectTab(item)">
        </sidebar-menu-item>
      </div>
      <div class="highlight-on-hover">
        <div class="seperator"></div>
        <h2>MANAGE</h2>
        <sidebar-menu-item v-for="item in this.manageItems" :key="name" :name="item" @click="selectTab(item)">
        </sidebar-menu-item>
      </div>
    </sidebar-menu>

  </div>
</template>

<script>
import SidebarMenu from './SidebarMenu.vue';
import SidebarMenuItem from './SidebarMenuItem.vue';

let menuItems = ['Albums', 'Playlists', 'Artists', 'Add Directory', 'Remove Directory'];
let libItems = menuItems.slice(0,3);
let manageItems = menuItems.slice(3,5);

export default {
  components: {
    SidebarMenu,
    SidebarMenuItem
  },
  data () {
    return {
      menuItems,
      libItems,
      manageItems
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/css/vars.scss';

#sidebar {
  width: $sidebar-width;
  height: 100%;
  overflow-y: auto;
  background: $grey;
  color: rgba(255,255,255,0.6);
  z-index: 1;
  box-shadow: inset $menu-shadow;
}

#logo {
  position: relative;
  padding: 50px 35px 0px 35px;
  font-weight: 900;
  #name {
    font-size: 50px;
    font-weight: 900;
    color: rgba(255,255,255,0.8);
  }
  #ui {
    position: absolute;
    font-size: 85px;
    font-weight: 900;
    transform: translate(140px, -131px);

    // gradient in text => only in webkit
    background-size: 400% 400%;
    background: linear-gradient(60deg, #00A8C5, #FFFF7E);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
}
</style>
