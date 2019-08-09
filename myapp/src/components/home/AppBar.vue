<template>
  <v-app-bar app>
    <v-app-bar-nav-icon
            @click="toggleNavDrawer"
    ></v-app-bar-nav-icon>
    <v-toolbar-title>Andrew Kincaid</v-toolbar-title>
    <v-spacer></v-spacer>

    <v-btn
      icon
      @click="goToUserLoginHomepage"
    >
        <v-icon>{{ svgIcon }}</v-icon>
    </v-btn>
    <v-menu>

    </v-menu>
  </v-app-bar>
</template>

<script>
  import { mdiAccountCircle } from '@mdi/js';
  import { mapState } from 'vuex';

  export default {
      name: "AppBar",
      data: () => ({
          svgIcon: mdiAccountCircle,
      }),
      computed: {
        ...mapState({
            user: state => state.user,
        })
      },
      methods: {
          toggleNavDrawer () {
              this.$store.commit('toggleNavBar');
          },
          goToUserLoginHomepage () {
              if (this.user == null) {
                  this.$router.push({name: 'Login'});
              }
          }
      },
  }
</script>

<style scoped>

</style>