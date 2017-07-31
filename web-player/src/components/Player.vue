<template>
<div id="player" :style="this.playerStyleObject">
  <div class="artwork" :style="this.artStyleObject"></div>
  <div class="info">
    <div class="player-song" :style="this.songNameStyleObject">{{ this.details.songName }}</div>
    <div class="player-artist">{{ this.details.artist }}</div>
  </div>
  <audio :src="`http://localhost:3000/api/song/${this.details.songId}`" autoplay></audio>
  <div id="custom-player">
    <button id="prev" class="generic-p-bttn queue-bttn" :style="this.bttnStyleObject" @click="prevSong"></button>
    <button v-if="!this.playing" @click="play" id="play-bttn" class="generic-p-bttn" :style="this.bttnStyleObject"></button>
    <button v-if="this.playing" @click="pause" id="pause-bttn" class="generic-p-bttn" :style="this.bttnStyleObject"></button>
    <button id="next" class="generic-p-bttn queue-bttn" :style="this.bttnStyleObject" @click="nextSong"></button>
    <div id="duration">
      {{ secToMin(currentTime)}} / {{ secToMin(duration) }}
    </div>
    <div id="timeline" @click="this.moveScrubber">
      <div id="scrubber" :style="this.scrubberStyle"></div>
    </div>
    </div>
  </div>
</div>
</div>
</template>

<script>
import bus from './bus.js';

export default {
  mounted() {
    bus.$on('play-song', this.updateSong);
    this.audioEl = this.$el.querySelector('audio');
    this.scrubberEl = this.$el.querySelector('#scrubber');
    this.timelineEl = this.$el.querySelector('#timeline');

    this.timelineWidth = this.timelineEl.offsetWidth - this.scrubberEl.offsetWidth;
    this.scrubberWidth = this.scrubberEl.offsetWidth;

    this.audioEl.addEventListener('loadedmetadata', () => {
      this.duration = this.audioEl.duration;
      this.playing = true;
    });
    this.scrubberEl.addEventListener('mousedown', this.scrubberHold);
    window.addEventListener('mouseup', this.scrubberRelease);
    window.addEventListener('keydown', e => {
      if (e.keyCode === 32) {
        e.preventDefault();
        if (this.playing) this.pause();
        else this.play();
        return false;
      }
      else if (e.keyCode === 39) {
        bus.$emit('next-song');
      }
      else if (e.keyCode === 37) {
        bus.$emit('prev-song');
      }
    });
    //window.addEventListener('')

    this.updatingTime = this.updateTime();
    this.duration = this.audioEl.duration;
    this.currentTime = 0;
    this.scrubbing = false; // true if user is dragging scrubber

    this.updatingTime = setInterval(this.updateTime, 100);
  },
  props: {
    details: { required: true }
  },
  methods: {
    play() {
      this.playing = true;
      this.audioEl.play();
    },
    pause() {
      this.playing = false;
      this.audioEl.pause();
    },
    nextSong() {
      bus.$emit('next-song');
    },
    prevSong() {
      bus.$emit('prev-song');
    },
    moveScrubber(e) {
      this.audioEl.currentTime = this.duration * this.clickPercent(e);

      let left = e.clientX - this.getPos(this.timelineEl);

      if (left >= 0 && left <= this.timelineWidth) {
        this.scrubberStyle.transform = `translate(${left}px, -5px)`;
      }
      else if (left < 0) {
        this.scrubberStyle.transform = `translate(0px, -5px)`;
      }
      else if (left > this.timelineWidth) {

        this.scrubberStyle.transform = `translate(${this.timelineWidth}px, -5px)`;
      }
    },
    scrubberHold(e) {
      this.scrubbing = true;
      this.moveScrubber(e);
      window.addEventListener('mousemove', this.moveScrubber);
      clearInterval(this.updatingTime);
    },
    scrubberRelease(e) {
      if (this.scrubbing) {
        this.scrubbing = false;
        this.moveScrubber(e);
        window.removeEventListener('mousemove', this.moveScrubber);
        this.audioEl.currentTime = this.duration * this.clickPercent(e);
        this.updatingTime = setInterval(this.updateTime, 100);
      }

    },
    updateTime() {
      let newTime = this.audioEl.currentTime;
      this.currentTime = newTime;
      let pixelsPlayed = this.timelineWidth * (newTime / this.duration);
      this.scrubberStyle.transform = `translate(${pixelsPlayed}px, -5px)`;
      if (newTime === this.duration && this.duration !== 0) {
        this.playing = false;
        bus.$emit('next-song');
      }
    },
    getPos(el) {
      return el.getBoundingClientRect().left;
    },
    clickPercent(e) {
      return (e.clientX - this.getPos(this.timelineEl)) / this.timelineWidth;
    },
    updateSong(song) {
      this.songData = song;
      this.artStyleObject.background = `url(${song.albumData.art.large})`;

      let palette = song.albumData.artPalette;
      this.artStyleObject.border = palette.muted === 'undefined' ? '6px solid #303030' : `6px solid rgb(${palette.lightMuted})`;
      this.playerStyleObject.background = palette.darkMuted === 'undefined' ? '#212121' : `rgb(${palette.darkMuted})`;
      this.songNameStyleObject.color = palette.lightVibrant === 'undefined' ? '#f2f2f2' :  `rgb(${palette.lightVibrant})`;
      this.bttnStyleObject.background = palette.lightVibrant === 'undefined' ? '#f2f2f2' :  `rgb(${palette.lightVibrant})`;
      this.scrubberStyle.background = palette.lightVibrant === 'undefined' ? '#f2f2f2' :  `rgb(${palette.lightVibrant})`;

      //this.songNameStyleObject.color = palette.muted === 'undefined' ? '#303030' : `rgb(${palette.lightMuted})`;
      //this.bttnStyleObject.background = palette.muted === 'undefined' ? '#303030' : `rgb(${palette.lightMuted})`;
      //this.scrubberStyle.background = palette.muted === 'undefined' ? '#303030' : `rgb(${palette.lightMuted})`;
      //this.playerStyleObject.background = `linear-gradient(135deg, rgb(${song.albumData.artPalette.darkMuted}), #212121)`
    },
    secToMin(s) {
      s = Number(s);
      let m = Math.floor(s % 3600 / 60);
      let _s = Math.floor(s % 3600 % 60);
      if (_s < 10) {
        _s = `0${_s}`;
      }
      return `${m}:${_s}`
    }
  },
  data () {
    return {
      playing: true,
      duration: 0,
      currentTime: 0,
      songData: this.details,
      scrubberStyle: {
        transform: `translate(0px, -5px)`,
        background: `rgb(${this.details.albumData.artPalette.lightVibrant})`
      },
      artStyleObject: {
        background: `url(${this.details.albumData.art.large})`,
        border: `6px solid rgba(${this.details.albumData.artPalette.muted}, 0.8)`,
      },
      playerStyleObject: {
        background: `rgb(${this.details.albumData.artPalette.darkMuted})`
        //background: `linear-gradient(135deg, rgb(${this.details.albumData.artPalette.darkMuted}), #212121)`
      },
      songNameStyleObject: {
        color: `rgb(${this.details.albumData.artPalette.lightVibrant})`
      },
      bttnStyleObject: {
        background: `rgb(${this.details.albumData.artPalette.lightVibrant})`
      }
    }
  }

}
</script>

<style lang="scss" scoped>
@import '../assets/css/vars.scss';

#custom-player {
  width: calc(100% - #{$sidebar-width});
  height: 100px;
  position: absolute;
  left: 0;
  margin-left: $sidebar-width;
  top: 0;
  text-align: center;
  //background: green;
}

#scrubber {
  position: absolute;
  height: 15px;
  width: 15px;
  border-radius: 50%;
  cursor: pointer;
  background: #f2f2f2;
  //transition: 0.1s linear;
  transition: height 0.1s ease, width 0.1s ease, margin-top 0.1s ease;
}
#timeline:hover #scrubber, #scrubber:hover, #scrubber:focus {
  height: 20px;
  width: 20px;
  margin-top: -2px;
  box-shadow: 0px 0px 51px 0px rgba(0, 0, 0, 0.1), 0px 3px 18px 0px rgba(0, 0, 0, 0.2);
}


#timeline {
  width: calc(100% - 40px);
  height: 7px;
  background: rgba(0,0,0,0.4);
  margin-top: 15px;
  margin-left: 0px;
  border-radius: 2px;
}

#duration {
  position: absolute;
  right: 40px;
  bottom: 31px;
  font-size: 16px;
  font-weight: 700;
}

.generic-p-bttn {
  display: inline-block;
  height: 50px;
  width: 50px;
  margin-top: 20px;
  border-radius: 50%;
  background: #d2d2d2;
  outline: none;
  border: none;
  cursor: pointer;
  box-shadow: 0px 0px 51px 0px rgba(0, 0, 0, 0.02), 0px 3px 18px 0px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease, background 1s ease;
}

.generic-p-bttn:hover {
  transform: scale(1.1);
  background: #f2f2f2;
  box-shadow: 0px 0px 51px 0px rgba(0, 0, 0, 0.1), 0px 3px 18px 0px rgba(0, 0, 0, 0.2);
}
.generic-p-bttn:active {
  transform: scale(1);
}

.queue-bttn {
  width: 35px;
  height: 35px;
  position: absolute;
  top: 8px;
}
#next {
  margin-left: 30px;
}
#prev {
  margin-left: -70px;
}

#next::after {
  content: '';
  height: 15px;
  width: 15px;
  background: url('../assets/img/play.png');
  background-size: cover;
  background-position: center center;
  opacity: 0.7;
  position: absolute;
  margin-top: -8px;
  margin-left: -6px;
}
#prev::after {
  content: '';
  height: 15px;
  width: 15px;
  background: url('../assets/img/play.png');
  background-size: cover;
  background-position: center center;
  opacity: 0.7;
  position: absolute;
  margin-top: -8px;
  margin-left: -9px;
  transform: rotate(180deg);
}


#play-bttn::after {
  content: '';
  width: 22px;
  height: 22px;
  margin-top: -11px;
  margin-left: -9px;
  background: url('../assets/img/play.png');
  background-size: cover;
  background-position: center center;
  position: absolute;
  opacity: 0.7;
  transition: 0.2s ease;
}
#play-bttn:hover::after {
  transform: scale(1);
}

#pause-bttn::after {
  content: '';
  width: 22px;
  height: 22px;
  margin-top: -11px;
  margin-left: -11px;
  background: url('../assets/img/pause.png');
  background-size: cover;
  background-position: center center;
  position: absolute;
  opacity: 0.7;
  transition: 0.2s ease;
}
#pause-bttn:hover::after {
  transform: scale(1.0);
}

#player {
  position: absolute;
  height: $player-height;
  width: 100%;
  background: #212121;
  bottom: 0;
  left: 0;
  margin-top: -100px;
  z-index: 2;
  box-shadow: 0px 0px 51px 0px rgba(0, 0, 0, 0.15), 0px 3px 18px 0px rgba(0, 0, 0, 0.3);
  transition: background 1s ease, color 1s ease, transform 0.4s ease;

}
.artwork {
  transition: 0.6s ease;
  height: calc(#{$player-height} + 75px);
  width: calc(#{$player-height} + 75px);
  margin-top: -90px;
  margin-left: calc(#{$sidebar-width}/2 - #{$player-height}/2 - 37px);
  //margin-left: 25px;
  background-size: cover !important;
  background-position: center center !important;
  box-shadow: 0px 0px 51px 0px rgba(0, 0, 0, 0.1), 0px 3px 18px 0px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
  position: absolute;
  z-index: 2;
  -webkit-backface-visibility: hidden;
}
/*
.artwork::after {
  content: '';
  position: absolute;
  width: calc(100% + 16px);
  height: calc(100% + 16px);
  margin-left: -8px;
  margin-top: -8px;
  //background: rgba(255,255,255,0.1);
}
*/
.artwork-bg {
  height: calc(#{$player-height} + 71px);
  width: calc(#{$player-height} + 71px);
  position: absolute;
  margin-top: -83px;
  margin-left: calc(#{$sidebar-width}/2 - 85px);
  background-size: cover;
  background-position: center center;
  border-radius: 12px;
  box-shadow: 0px 0px 51px 0px rgba(0, 0, 0, 0.1), 0px 3px 18px 0px rgba(0, 0, 0, 0.2);

}
.artwork-bg::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.7);
  border-radius: 12px;
}

.info {
  margin-left: $sidebar-width;
  margin-top: 18px;

  .player-song {
    font-size: 22px;
    font-weight: 900;
    margin-bottom: 7px;
    width: calc(50% - 130px);
    //padding-right: 45px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    transition: 1s ease;
  }
  .player-artist {
    font-size: 16px;
    font-weight: 700;
    width: calc(50% - 130px);
    //padding-right: 30px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    transition: 1s ease;
  }
}
audio {
  position: absolute;
  right: 0;
  top: 0;
  //display: none;
}

.play{background: url('http://www.alexkatz.me/codepen/img/play.png') ;}
.pause{background: url('http://www.alexkatz.me/codepen/img/pause.png') ;}


</style>
