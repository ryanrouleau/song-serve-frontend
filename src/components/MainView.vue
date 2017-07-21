<template>
  <div id="main-view">
  </div>
</template>

<script>

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
  box-shadow: 0px 0px 0px 0px rgba(155,155,155,0.5);
}
</style>
