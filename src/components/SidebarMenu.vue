<template>
  <div class="sidebar-menu">
    <div class="seperator"></div>
    <div class="highlight-on-hover">
      <h2>LIBRARY</h2>
      <sidebar-menu-item v-for="(item, index) in this.libItems" :selected="(index === 0) ? true : false" :key="item" :name="item" @click.native="selectTab(item)">
      </sidebar-menu-item>
    </div>

    <div class="seperator"></div>

    <div class="highlight-on-hover">
      <h2>MANAGE</h2>
      <sidebar-menu-item v-for="item in this.manageItems" :key="item" :name="item" @click.native="selectTab(item)">
      </sidebar-menu-item>
    </div>
    <div class="seperator"></div>
  </div>
</template>

<script>
import SidebarMenuItem from './SidebarMenuItem.vue';
import bus from './bus.js';

let menuItems = ['Albums', 'Artists', 'Playlists', 'Add Directory', 'Remove Directory'];
let libItems = menuItems.slice(0,3);
let manageItems = menuItems.slice(3,5);

export default {
  created() {
    console.log(this.$children);
    this.children = this.$children;
    this.selectTab('Albums');
  },
  components: {
    SidebarMenuItem
  },
  data () {
    return {
      menuItems,
      libItems,
      manageItems
    }
  },
  methods: {
    selectTab(selectedItem) {
      let prevSelected = '';
      this.children.forEach(child => {
        if (child.isActive) prevSelected = child.name;
        child.isActive = (child.name === selectedItem);
      });
      if (prevSelected != selectedItem) bus.$emit('tab-changed', selectedItem);
    },
    selectDefaultTabOnLoad(defaultTab) {
      this.selectTab(defaultTab);
    }
  }
}
</script>

<style lang="scss">
@import '../assets/css/vars.scss';

.sidebar-menu {
  padding: 0px 35px 0px 35px;

  h2 {
    font-weight: 900;
    padding-bottom: 20px;
    font-size: 24px;
  }
}
.seperator {
  width: calc(100% + 70px);
  height: 1px;
  margin: 30px 0px 40px -35px;
  background: rgba(255,255,255,0.05);
  //box-shadow: $menu-shadow;
}
.seperator:last-of-type {
  margin-bottom: 0px;
}
.highlight-on-hover {
  h2 {
    transition: 0.3s ease;
  }
}
.highlight-on-hover:hover {
  h2 {
    color: rgba(255,255,255,0.9);
  }
}
</style>
