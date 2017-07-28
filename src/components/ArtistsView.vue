<template>
  <div class="main-view">
    <div class="main-view-header">
      <h1 class="main-view-title">Artists <span class="num-albums">Dispalying <span class="bold">{{ numberOfArtists }}</span> artists</span></h1>
    </div>
    <div class="grid" id="artist-grid">
      <artist v-for="artist in this.artists" :key="artist.id" :details="artist"></artist>
    </div>
  </div>
</template>

<script>
import Artist from './Artist.vue';
import axios from 'axios';

export default {
  created () {
    this.artists = [];
    this.getArtists();
  },
  data () {
    return {
      numberOfArtists: 0
    }
  },
  methods: {
    getArtists() {
      axios.get('http://localhost:3000/api/artists').then(res => {
        res.data.artists.forEach(artist => {
          if (artist.art.small !== 'undefined') this.artists.push(artist);
        })
        this.numberOfArtists = this.artists.length;
        //this.numberOfArtists = res.data.numberOfArtists;
      })
      .catch(err => {
        alert(err);
      });
    }
  },
  components: {
    Artist
  }
}
</script>

<style lang="scss">

</style>
