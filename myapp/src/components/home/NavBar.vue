<template>
  <v-navigation-drawer
      app
      clipped
      :value="navBarVisible"
  >
    <v-list
        dense
        nav
        class="py-0"
    >
      <v-list-item two-line>
        <v-list-item-avatar>
          <img src="https://randomuser.me/api/portraits/men/81.jpg">
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>Application</v-list-item-title>
          <v-list-item-subtitle>Subtext</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

<!--      <v-list-item-->
<!--          v-for="item in items"-->
<!--          :key="item.title"-->
<!--          link-->
<!--      >-->
<!--        <v-list-item-icon>-->
<!--          <v-icon>{{ item.icon }}</v-icon>-->
<!--        </v-list-item-icon>-->

<!--        <v-list-item-content>-->
<!--          <v-list-item-title>{{ item.title }}</v-list-item-title>-->
<!--        </v-list-item-content>-->
<!--      </v-list-item>-->
    </v-list>

  </v-navigation-drawer>
</template>

<script>
    import { mapState } from 'vuex';

    export default {
        name: "NavBar",
        computed: {
          ...mapState({
              navBarVisible: state => state.navBarVisible,

          })
        }
    }
</script>

<style scoped>

</style>