<template>
  <div :class="{ 'selected' : this.selected }" class="sidebar-menu-item">
    {{ this.name }}
  </div>
</template>

<script>

export default {
  data () {
    return {
      isActive: false
    }
  },
  props: {
    selected: { default: false },
    name: {required: true}
  },
  mounted() {
    this.isSelected = this.selected;
  }
}
</script>

<style lang="scss">
@import '../assets/css/vars.scss';

.sidebar-menu-item {
  font-size: 18px;
  font-weight: 700;
  width: calc(100% + 35px);
  margin-right: -35px;
  padding: 15px 5px;
  margin: 10px 0px;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
  cursor: pointer;
  transition: 0.1s ease;
}
.sidebar-menu-item:hover {
  color: $off-white;
  background: rgba(255,255,255,0.1);
  padding-left: 20px;
}
.sidebar-menu-item.selected {
  background: $light-grey;
  color: $off-white;
  box-shadow: $menu-shadow;
  padding-left: 20px;
  margin-top: 15px;
  margin-bottom: 15px;
}
</style>
