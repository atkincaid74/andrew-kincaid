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
                    <UserIcon></UserIcon>
                </v-list-item-avatar>

                <v-list-item-content>
                    <v-list-item-title>{{ fullName }}</v-list-item-title>
                    <v-list-item-subtitle>{{ username }}</v-list-item-subtitle>
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
    import UserIcon from "./UserIcon";

    export default {
        name: "NavBar",
        components: {
            UserIcon,
        },
        computed: {
            ...mapState({
                navBarVisible: state => state.navBarVisible,
                username: state => state.username,
                userFirstName: state => state.userFirstName,
                userLastName: state => state.userLastName,
            }),
            fullName () {
                return this.userFirstName + ' ' + this.userLastName
            },
            userIcon () {
                return !!this.username ? mdiAccountCircle : mdiAccountCircleOutline
            }
        }
    }
</script>

<style scoped>

</style>