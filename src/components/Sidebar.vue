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

    <side-menu name="LIBRARY">
    </side-menu>

    <side-menu name="MANAGEMENT">
    </side-menu>

  </div>
</template>

<script>
import SideMenu from './SideMenu.vue';

export default {
  components: {
    SideMenu
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/css/vars.scss';

#sidebar {
  width: 300px;
  height: 100%;
  background: $grey;
  color: rgba(255,255,255,0.6);
}

#logo {
  padding: 30px;
  font-weight: 900;
  #name {
    font-size: 50px;
    color: rgba(255,255,255,0.8);
  }
  #ui {
    position: absolute;
    font-size: 85px;
    transform: translate(144px, -131px);

    // gradient in text => only in webkit
    background-size: 400% 400%;
    background: linear-gradient(60deg, #00A8C5, #FFFF7E);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
}
</style>
