<template>
    <v-snackbar
        v-model="displaySnackbar"
        :color="snackbarColor"
        :timeout="timeout"
        top
    >
        {{ snackbarMessage }}
        <v-btn
            dark
            text
            @click="toggleSnackbar"
        >Close</v-btn>
    </v-snackbar>
</template>

<script>
    import { mapState } from 'vuex';

    export default {
        name: "Snackbar",
        data: () => ({
            timeout: 6000
        }),
        computed: {
            ...mapState({
                displaySnackbar: state => state.displaySnackbar,
                snackbarMessage: state => state.snackbarMessage,
                snackbarColor: state => state.snackbarColor,
            }),
            displaySnackbar: {
                get () {
                    return this.$store.state.displaySnackbar
                },
                set () {
                    return this.$store.commit('toggleDisplaySnackbar')
                }
            }
        },
        methods: {
            toggleSnackbar () {
                this.$store.commit('toggleDisplaySnackbar');
            }
        },
    }
</script>

<style scoped>

</style>