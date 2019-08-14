<template>
    <v-app-bar app>
        <v-app-bar-nav-icon
            @click="toggleNavDrawer"
        ></v-app-bar-nav-icon>
        <v-toolbar-title>
            <v-btn
                text
                @click="goHome"
            > Andrew Kincaid </v-btn>
        </v-toolbar-title>
        <v-spacer></v-spacer>

        <v-btn
            v-if="this.username === null"
            icon
            @click="goToUserLoginHomepage"
        >
            <UserIcon></UserIcon>
        </v-btn>

        <v-menu
            v-if="this.username !== null"
            v-model="menu"
            :close-on-click="true"
            :close-on-content-click="true"
        >
            <template v-slot:activator="{ on }">
                <v-btn
                    icon
                    v-on="on"
                >
                    <UserIcon></UserIcon>
                </v-btn>
            </template>
            <v-list>
                <v-list-item
                    @click="goToUserLoginHomepage"
                >User Homepage</v-list-item>
                <v-list-item
                    @click="logout"
                >Logout</v-list-item>
            </v-list>
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
            menu: false,

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
            },
            logout () {
                this.$store.dispatch('logout');
                this.$router.push({name: 'Home'})
            },
        },
    }
</script>

<style scoped>

</style>