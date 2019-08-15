<template>
    <v-dialog
            v-model="display"
            max-width="600"
            class="mx-auto"
            persistent
    >
        <v-card>
            <v-card-title>Create New User</v-card-title>
            <v-card-text>
                <v-form>
                    <v-layout row>
                        <v-flex lg6>
                            <v-text-field
                                    required
                                    v-model="firstName"
                                    label="First Name"
                                    @change="$v.firstName.$touch()"
                                    @blur="$v.firstName.$touch()"
                                    :error-messages="firstNameErrors"
                            ></v-text-field>
                        </v-flex>
                        <v-flex lg6>
                            <v-text-field
                                    required
                                    v-model="lastName"
                                    label="Last Name"
                                    @change="$v.lastName.$touch()"
                                    @blur="$v.lastName.$touch()"
                                    :error-messages="lastNameErrors"
                            ></v-text-field>
                        </v-flex>
                        <v-flex lg6>
                            <v-text-field
                                    required
                                    v-model="email"
                                    label="Email"
                                    @change="$v.email.$touch()"
                                    @blur="$v.email.$touch()"
                                    :error-messages="emailErrors"
                            ></v-text-field>
                        </v-flex>
                        <v-flex lg6>
                            <v-text-field
                                    required
                                    v-model="username"
                                    label="Username"
                                    @change="$v.username.$touch()"
                                    @blur="$v.username.$touch()"
                                    :error-messages="usernameErrors"
                            ></v-text-field>
                        </v-flex>
                        <v-flex lg6>
                            <v-text-field
                                    required
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
                                    required
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
                        @click="closeDialog"
                        color="red"
                >Close</v-btn>
                <v-btn
                        color="primary"
                        @click="createNewUser"
                        :disabled="formInvalid"
                >Submit</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    import { validationMixin } from 'vuelidate';
    import { required, minLength, maxLength, sameAs, email } from 'vuelidate/lib/validators';

    export default {
        name: "NewUser",
        props: {
            display: {type: Boolean, required: true}
        },
        mixins: [validationMixin],
        validations: {
            firstName: { required },
            lastName: { required },
            username: {required, minLength: minLength(4), maxLength: maxLength(16) },
            password: {required, minLength: minLength(6), maxLength: maxLength(32) },
            confirmPassword: { required, sameAsPassword: sameAs('password') },
            email: { required, email }
        },
        data: () => ({
            firstName: '',
            lastName: '',
            email: '',
            username: '',
            password: '',
            confirmPassword: '',
        }),
        computed: {
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
                !this.$v.confirmPassword.sameAsPassword && errors.push('Passwords do not match');
                return errors
            },
            emailErrors() {
                const errors = [];
                if (!this.$v.email.$dirty) return errors;
                !this.$v.email.email && errors.push('Invalid email');
                return errors
            },
            formInvalid() {
                return this.$v.$invalid
            }
        },
        methods:{
            createNewUser() {
                const payload = {
                    firstName: this.firstName,
                    lastName: this.lastName,
                    username: this.username,
                    password: this.password,
                    email: this.email,
                };
                this.$store.dispatch('createNewUser', payload)
                    .then(this.closeDialog)
            },
            closeDialog() {
                this.$emit('close-new-user', 'toggleCreateUserDialog')
            }
        }
    }
</script>

<style scoped>

</style>