<template>
    <div>
        <v-container>
            <v-row justify="center">
                <v-col cols="10">
                    <v-data-table
                        :headers="headers"
                        :items="users"
                        disable-pagination
                        hide-default-footer
                    ></v-data-table>
                </v-col>
            </v-row>
        </v-container>
        <v-container v-if="username === 'jojo69'">
            <v-row justify="center">
                <v-col cols="10">
                    <v-data-table
                        :headers="headersJojo"
                        :items="dataJojo"
                        disable-pagination
                        hide-default-footer
                    ></v-data-table>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
    import { mapState } from 'vuex';

    export default {
        name: "UserHomepage",
        computed: {
            ...mapState({
                username: state => state.username,
                userFirstName: state => state.userFirstName,
                userLastName: state => state.userLastName,
                userPaid: state => state.userPaid,
            }),
            users() {
                return [
                    {
                        user: this.username,
                        first: this.userFirstName,
                        last: this.userLastName,
                        paid: this.paid,
                    },
                ];
            }
        },
        data: () => ({
            headers: [
                {text: 'Username', value: 'user'},
                {text: 'First Name', value: 'first'},
                {text: 'Last Name', value: 'last'},
                {text: 'Paid', value: 'paid'},
            ],
            headersJojo: [
                {text: 'Joanne', value: 'jojo', align: 'center'},
                {text: 'Category', value: 'cat', align: 'center'},
                {text: 'Andrew', value: 'andy', align: 'center'},
            ],
            dataJojo: [
                {
                    jojo: 'Yes',
                    cat: 'Prettiest ever?',
                    andy: 'No',
                },
                {
                    jojo: 'Yes',
                    cat: 'As cute as it gets?',
                    andy: 'No',
                },
                {
                    jojo: 'Yes',
                    cat: 'The most fun?',
                    andy: 'No',
                },
                {
                    jojo: 'Yes',
                    cat: 'The sweetest?',
                    andy: 'No',
                },
                {
                    jojo: 'Yes',
                    cat: 'Knows all of the Lil\' Jon?',
                    andy: 'No',
                },
                {
                    jojo: 'Yes',
                    cat: 'Pro kickballer?',
                    andy: 'No',
                },
                {
                    jojo: 'Yes',
                    cat: 'Has the cutest butt?',
                    andy: 'No',
                },
                {
                    jojo: '7',
                    cat: 'Final Score',
                    andy: '0',
                },
                {
                    jojo: 'Yes',
                    cat: 'Clearly the best ever?',
                    andy: 'No',
                },
            ]
        }),
    }
</script>

<style scoped>

</style>