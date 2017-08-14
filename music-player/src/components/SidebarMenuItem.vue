<template>
  <div :class="{ 'selected' : this.isActive }" class="sidebar-menu-item">
    {{ this.name }}
  </div>
</template>

<script>

export default {
  props: {
    selected: { default: false },
    name: {required: true}
  },

  data () {
    return {
      isActive: this.selected
    }
  },
  methods: {
  }
}
</script>

<style lang="scss">
@import '../assets/css/vars.scss';

.sidebar-menu-item {
  font-size: 18px;
  font-weight: 700;
  width: calc(100% + 70px);
  padding: 15px 40px;
  margin: 10px 0px 10px -35px;
  cursor: pointer;
  transition: 0.1s ease;
}
.sidebar-menu-item:hover {
  color: $off-white;
  background: rgba(255,255,255,0.02);
  padding-left: 45px;
}
.sidebar-menu-item.selected {
  background: $light-grey;
  color: $off-white;
  //box-shadow: $menu-shadow;
  padding-left: 45px;
  //margin-top: 15px;
  //margin-bottom: 15px;
}
</style>
