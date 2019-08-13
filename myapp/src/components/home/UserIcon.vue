<template>
    <v-icon>{{ userIcon }}</v-icon>
</template>

<script>
    import { mdiAccountCircle, mdiAccountCircleOutline } from '@mdi/js';
    import { mapState } from 'vuex';

    export default {
        name: "UserIcon",
        computed: {
            ...mapState({
                username: state => state.username,
            }),
            userIcon() {
                return !!this.username ? mdiAccountCircle : mdiAccountCircleOutline
            },
        },

    }
</script>

<style scoped>

</style>