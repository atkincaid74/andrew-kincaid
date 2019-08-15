<template>
  <v-app>
    <Snackbar></Snackbar>
    <NavBar></NavBar>
    <AppBar></AppBar>
    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld';
import AppBar from "./components/home/AppBar";
import NavBar from "./components/home/NavBar";
import Snackbar from "./components/home/Snackbar";

export default {
  name: 'App',
  components: {
    HelloWorld,
    AppBar,
    NavBar,
    Snackbar,
  },
  data: () => ({

  }),
};
</script>
