<template>
  <div id="app">
    <p> FROM :</p>
    <select class="input-text" @click="getMessage()" v-model="markerLoc"  @change="selectFrom($event)">
      <option>please select one</option>
      <option v-for="coordinate in Coordinates" :key="coordinate" :value="coordinate">               
          {{coordinate.province}} 
         </option>
    </select>
    <p>TO :</p>
    <select class="input-text" @click="getMessage()" v-model="destinationLoc" @change="selectTo($event)">
      <option>please select one</option>
      <option v-for="coordinate in Coordinates" :key="coordinate" :value="coordinate">
        {{coordinate.province}}</option>
    </select>
    <!-- <select class="input-text" @click="getMessage()" v-model="destinationLoc.lng" @change="selectTo($event)">
      <option>please select one</option>
      <option v-for="coordinate in Coordinates" :key="coordinate.lng" :value="coordinate.lng">
        {{coordinate.province}}</option>
    </select> -->
  </div>
  <br>
  <div @click="moveMarker()" class="np-button">Fly Plane</div> <br>
  <div id="animated-marker-map" class="map-margins"></div> 
</template> 
<script>
import loadGoogleMapsApi from "load-google-maps-api";
import axios from 'axios'

export default {
  name: "GoogleMap",
  data() {
    return {
      markerLoc: {
        lat: null,
        lng: null
      },
      destinationLoc: {
        lat: null,
        lng: null
      },
      Coordinates: [],
      lngCoordinates: [],
      latCoordinates: [],
      map: null,
      marker: null,
      centerLoc: { lat: 38.9637, lng: 35.2433 },
    };
  },

  mounted() {
    loadGoogleMapsApi({
      key: "AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNGg",
      libraries: ["places", "geometry"],
    }).then(async () => {
      const mapZoom = 6;
      const { google } = window;
      const mapOptions = {
        zoom: mapZoom,
        mapTypeId: google.maps.MapTypeId.HYBRID,

        // Initialised the marker
        center: new google.maps.LatLng({
          lat: this.centerLoc.lat,
          lng: this.centerLoc.lng,
        }),
        mapTypeControl: true,
        streetViewControl: false,
      };

      this.map = new google.maps.Map(
        document.getElementById("animated-marker-map"),
        mapOptions
      );
      const planeIcon = {
        url: "https://img.icons8.com/external-icongeek26-glyph-icongeek26/64/000000/external-airplane-transportation-icongeek26-glyph-icongeek26-4.png",
        anchor: new google.maps.Point(25, 50),
        scaledSize: new google.maps.Size(50, 50),
      };

      this.marker = new google.maps.Marker({
        position: this.$markerLoc,
        map: this.map,
        icon: planeIcon,
      });
    });
  },

  methods: {
    getMessage() {
      const path = 'http://localhost:5000/test2';
      axios.get(path)
        .then((res) => {
          this.Coordinates = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    created() {
      this.getMessage();
    },

    selectFrom(event1) {
      console.log(event1.target.value);
    },
    selectTo(event2) {
      console.log(event2.target.value);
    },

    latBiggerLng() {
      this.markerLoc.lat -= 0.001;
      this.markerLoc.lng += 0.001;
      this.markerLoc.lat = parseFloat(this.markerLoc.lat);
      this.markerLoc.lng = parseFloat(this.markerLoc.lng);
    },

    latLngBig() {
      this.markerLoc.lat -= 0.001;
      this.markerLoc.lng -= 0.001;
      this.markerLoc.lat = parseFloat(this.markerLoc.lat);
      this.markerLoc.lng = parseFloat(this.markerLoc.lng);
    },

    latLngSmall() {
      this.markerLoc.lat += 0.001;
      this.markerLoc.lng += 0.001;
      this.markerLoc.lat = parseFloat(this.markerLoc.lat);
      this.markerLoc.lng = parseFloat(this.markerLoc.lng);
    },

    latSmallerLng() {
      this.markerLoc.lat += 0.001;
      this.markerLoc.lng -= 0.001;
      this.markerLoc.lat = parseFloat(this.markerLoc.lat);
      this.markerLoc.lng = parseFloat(this.markerLoc.lng);
    },

    latSmallLngEqual() {
      this.markerLoc.lat += 0.001;
      this.markerLoc.lng == 0.001;
      this.markerLoc.lat = parseFloat(this.markerLoc.lat);
      this.markerLoc.lng = parseFloat(this.markerLoc.lng);
    },

    lngSmallLatEqual() {
      this.markerLoc.lat == 0.001;
      this.markerLoc.lng += 0.001;
      this.markerLoc.lat = parseFloat(this.markerLoc.lat);
      this.markerLoc.lng = parseFloat(this.markerLoc.lng);
    },

    latBigLngEq() {
      this.markerLoc.lat -= 0.001;
      this.markerLoc.lng == 0.001;
      this.markerLoc.lat = parseFloat(this.markerLoc.lat);
      this.markerLoc.lng = parseFloat(this.markerLoc.lng);
    },

    lngLatEq() {
      this.markerLoc.lat == 0.001;
      this.markerLoc.lng -= 0.001;
      this.markerLoc.lat = parseFloat(this.markerLoc.lat);
      this.markerLoc.lng = parseFloat(this.markerLoc.lng);
    },

    sleep(milliseconds) {
      return new Promise((resolve) => setTimeout(resolve, milliseconds));
    },

    async moveMarker() {

      this.loop = 0;
      while (this.loop < 1) {
        if (
          this.markerLoc.lat >= 44.444 ||
          this.markerLoc.lat <= 33.225 ||
          this.markerLoc.lng >= 52.068 ||
          this.markerLoc.lng <= 18.69
        ) {
          alert("Out of Map");
          this.markerLoc.lat -= 0.0001;
          this.markerLoc.lng -= 0.0001;
          return (this.loop = 1);
        } else {
          if (
            this.markerLoc.lat > this.destinationLoc.lat &&
            this.markerLoc.lng < this.destinationLoc.lng
          ) {
            this.latBiggerLng();
            await this.sleep(0);
          } else if (
            this.markerLoc.lat > this.destinationLoc.lat &&
            this.markerLoc.lng > this.destinationLoc.lng
          ) {
            this.latLngBig();
            await this.sleep(0);
          } else if (
            this.markerLoc.lat < this.destinationLoc.lat &&
            this.markerLoc.lng < this.destinationLoc.lng
          ) {
            this.latLngSmall();
            await this.sleep(0);
          } else if (
            this.markerLoc.lat < this.destinationLoc.lat &&
            this.markerLoc.lng > this.destinationLoc.lng
          ) {
            this.latSmallerLng();
            await this.sleep(0);
          } else if (
            this.markerLoc.lat < this.destinationLoc.lat &&
            this.markerLoc.lng == this.destinationLoc.lng
          ) {
            this.latSmallLngEqual();
            await this.sleep(0);
          } else if (
            this.markerLoc.lat == this.destinationLoc.lat &&
            this.markerLoc.lng < this.destinationLoc.lng
          ) {
            this.lngSmallLatEqual();
            await this.sleep(0);
          } else if (
            this.markerLoc.lat > this.destinationLoc.lat &&
            this.markerLoc.lng == this.destinationLoc.lng
          ) {
            this.latBigLngEq();
            await this.sleep(0);
          } else if (
            this.markerLoc.lat == this.destinationLoc.lat &&
            this.markerLoc.lng > this.destinationLoc.lng
          ) {
            this.lngBigLatEq();
            await this.sleep(0);
          } else if (
            this.markerLoc.lat == this.destinationLoc.lat &&
            this.markerLoc.lng == this.destinationLoc.lng
          ) {
            this.lngLatEq();
            await this.sleep(0);
          }
        }
        this.marker.setPosition(this.markerLoc)
      }
    },
  }
};
</script>

<style scoped>

p{
    font-weight: bold;
  font-family:Calibri;
}

select
{
    display: inline-block;
}

.input-text {
  border: none;
  background-color: #EEEEEE;
  height: 30px;
  border-radius: 3px;
  margin-right: 0.5rem;
  padding-left: 6px;
  font-family: Calibri;
  color: #495057;
}

.map-margins {
  height: 600px;
  width: 100%;
}

.np-button {
  width: 235px;
  background: rgb(12, 147, 34);
  color: #fff;
  border-radius: 6px;
  text-align: center;
  padding: 6px 6px;
  transition: all 0.3s;
  cursor: pointer;
  text-transform: uppercase;
  font-family: Calibri;
}

.np-button:hover {
  background: rgb(141, 183, 141);
  transition: all 0.3s;
}
</style>
