<template>
  <v-app-bar app>
    <v-app-bar-nav-icon
            @click="toggleNavDrawer"
    ></v-app-bar-nav-icon>
    <v-toolbar-title>
        <v-btn
            text
            @click="goHome"
        >
            Andrew Kincaid
        </v-btn>
    </v-toolbar-title>
    <v-spacer></v-spacer>

    <v-btn
      icon
      @click="goToUserLoginHomepage"
    >
        <UserIcon></UserIcon>
    </v-btn>
    <v-menu>

    </v-menu>
  </v-app-bar>
</template>

<script>
    import UserIcon from "./UserIcon";
    import { mapState } from 'vuex';

    export default {
        name: "AppBar",
        components: {
          UserIcon
        },
        data: () => ({

        }),
        computed: {
        ...mapState({
            username: state => state.username,
        })
        },
        methods: {
            toggleNavDrawer () {
              this.$store.commit('toggleNavBar');
            },
            goToUserLoginHomepage () {
              if (this.username == null) {
                  this.$router.push({name: 'Login'});
              } else {
                  this.$router.push({name: 'UserHome'})
              }
            },
            goHome () {
              this.$router.push({name: 'Home'});
            }
        },
    }
</script>

<style scoped>

</style>