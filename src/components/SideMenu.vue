<template>
  <div class="side-menu">
    <div class="seperator"></div>
    <h2>{{ this.name }}</h2>
  </div>
</template>

<script>

export default {
  props: {
    name: { required: true }
  }
}
</script>

<style lang="scss">
@import '../assets/css/vars.scss';

.side-menu {
  padding: 0px 30px;
  padding: 0px 30px 30px 30px;
  transition: 0.5s ease;

  .seperator {
    width: calc(100% + 60px);
    height: 4px;
    margin: 0px 0px 30px -30px;
    background: $light-grey;
  }
}
.side-menu:hover {
  color: rgba(255,255,255,0.9);
}
</style>
