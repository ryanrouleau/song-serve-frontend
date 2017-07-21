<template>
  <div class="sidebar-menu">
    <slot></slot>
  </div>
</template>

<script>
import SidebarMenuItem from './SidebarMenuItem.vue';

export default {
  created() {
    console.log(this.$children);
    this.menuItems = this.$children;
  },
  components: {
    SidebarMenuItem
  },
  data () {
    return {
    }
  },
  methods: {
    selectItem(selectedItem) {
      console.log(selectItem);
      this.menuItems.forEach(item => {
        item.isSelected = (item.name === selectItem.name);
      });
    }
  }
}
</script>

<style lang="scss">
@import '../assets/css/vars.scss';

.sidebar-menu {
  padding: 0px 35px 50px 35px;

  h2 {
    font-weight: 900;
    padding-bottom: 20px;
  }
  .seperator {
    width: calc(100% + 70px);
    height: 1px;
    margin: 30px 0px 40px -35px;
    //background: rgba(255,255,255,0.05);
    //box-shadow: $menu-shadow;
  }
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
