<template>
    <div>
        <v-card
            max-width="50%"
            class="mx-auto my-10"
        >
            <v-card-title>
                Login
            </v-card-title>
            <v-card-text>
                <v-form>
                    <v-text-field
                        v-model="enteredUser"
                        label="Username"
                        @submit=""
                        @keydown.enter.prevent=""
                        autofocus
                        @change="$v.enteredUser.$touch()"
                        @blur="$v.enteredUser.$touch()"
                        :error-messages="userErrors"
                    ></v-text-field>
                    <v-text-field
                            v-model="enteredPass"
                            label="Password"
                            type="password"
                            @submit=""
                            @keydown.enter.native=""
                            @change="$v.enteredPass.$touch()"
                            @blur="$v.enteredPass.$touch()"
                            :error-messages="passErrors"
                    ></v-text-field>
                </v-form>
            </v-card-text>
            <v-card-actions>
                <v-btn
                    @click="toggleCreateUserDialog"
                >Create Account</v-btn>
                <v-spacer></v-spacer>
                <v-btn
                        @click=""
                >Login
                </v-btn>
            </v-card-actions>
        </v-card>
        <v-dialog
            v-model="createUserDialog"
            max-width="50%"
            class="mx-auto"
            persistent
        >
            <v-card>
                <v-card-title>Create New User</v-card-title>
                <v-card-text>
                    <v-form>
                        <v-layout row>
                            <v-flex lg4>
                                <v-text-field
                                        v-model="firstName"
                                        label="First Name"
                                        @change="$v.firstName.$touch()"
                                        @blur="$v.firstName.$touch()"
                                        :error-messages="firstNameErrors"
                                ></v-text-field>
                            </v-flex>
                            <v-flex lg4>
                                <v-text-field
                                        v-model="lastName"
                                        label="Last Name"
                                        @change="$v.lastName.$touch()"
                                        @blur="$v.lastName.$touch()"
                                        :error-messages="lastNameErrors"
                                ></v-text-field>
                            </v-flex>
                            <v-flex lg4>
                                <v-text-field
                                        v-model="username"
                                        label="Username"
                                        @change="$v.username.$touch()"
                                        @blur="$v.username.$touch()"
                                        :error-messages="usernameErrors"
                                ></v-text-field>
                            </v-flex>
                            <v-flex lg6>
                                <v-text-field
                                        v-model="password"
                                        label="Password"
                                        type="password"
                                        @change="$v.password.$touch()"
                                        @blur="$v.password.$touch()"
                                        :error-messages="passwordErrors"
                                ></v-text-field>
                            </v-flex>
                            <v-flex lg6>
                                <v-text-field
                                        v-model="confirmPassword"
                                        label="Confirm Password"
                                        type="password"
                                        @change="$v.confirmPassword.$touch()"
                                        @blur="$v.confirmPassword.$touch()"
                                        :error-messages="confirmPasswordErrors"
                                ></v-text-field>
                            </v-flex>
                        </v-layout>
                    </v-form>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        @click="toggleCreateUserDialog"
                        color="red"
                    >Close</v-btn>
                    <v-btn
                        color="primary"
                    >Submit</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
    import { validationMixin } from 'vuelidate';
    import { required, minLength, maxLength, sameAs } from 'vuelidate/lib/validators';
    import { mapState } from 'vuex';

    export default {
        name: "Login",
        mixins: [validationMixin],
        validations: {
            enteredUser: { required, minLength: minLength(4) },
            enteredPass: { required, minLength: minLength(6), maxLength: maxLength(32) },
            firstName: { required },
            lastName: { required },
            username: {required, minLength: minLength(4), maxLength: maxLength(16) },
            password: {required, minLength: minLength(6), maxLength: maxLength(32) },
            confirmPassword: { required, sameAsPassword: sameAs('password') },
        },
        data: () => ({
            enteredUser: null,
            enteredPass: null,
            createUserDialog: false,
            firstName: '',
            lastName: '',
            username: '',
            password: '',
            confirmPassword: '',
        }),
        computed: {
            userErrors() {
                const errors = [];
                if (!this.$v.enteredUser.$dirty) return errors;
                !this.$v.enteredUser.minLength && errors.push('Username must be at least 4 characters');
                !this.$v.enteredUser.required && errors.push('Username is required');
                return errors
            },
            passErrors() {
                const errors = [];
                if (!this.$v.enteredPass.$dirty) return errors;
                !this.$v.enteredPass.minLength && errors.push('Password must be at least 6 characters');
                !this.$v.enteredPass.maxLength && errors.push('Password must be less than 32 characters');
                !this.$v.enteredPass.required && errors.push('Password is required');
                return errors
            },
            firstNameErrors() {
                const errors = [];
                if (!this.$v.firstName.$dirty) return errors;
                !this.$v.firstName.required && errors.push('First name is required');
                return errors
            },
            lastNameErrors() {
                const errors = [];
                if (!this.$v.lastName.$dirty) return errors;
                !this.$v.lastName.required && errors.push('Last name is required');
                return errors
            },
            usernameErrors() {
                const errors = [];
                if (!this.$v.username.$dirty) return errors;
                !this.$v.username.required && errors.push('Username is required');
                !this.$v.username.minLength && errors.push('Username must be at least 4 characters');
                !this.$v.username.maxLength && errors.push('Username must be less than 16 characters');
                return errors
            },
            passwordErrors() {
                const errors = [];
                if (!this.$v.password.$dirty) return errors;
                !this.$v.password.required && errors.push('Password is required');
                !this.$v.password.minLength && errors.push('Password must be at least 6 characters');
                !this.$v.password.maxLength && errors.push('Password must be less than 32 characters');
                return errors
            },
            confirmPasswordErrors() {
                const errors = [];
                if (!this.$v.confirmPassword.$dirty) return errors;
                !this.$v.confirmPassword.sameAsPassword && errors.push('Passwords do not match')
                return errors
            }
        },
        methods: {
            submitLoginInfo() {

            },
            toggleCreateUserDialog() {
                this.createUserDialog = !this.createUserDialog;
                console.log(this.createUserDialog);
            },
        },
    }
</script>

<style scoped>

</style>