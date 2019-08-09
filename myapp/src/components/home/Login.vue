<template>
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
            <v-btn>Create Account</v-btn>
            <v-spacer></v-spacer>
            <v-btn>Login</v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
    import { validationMixin } from 'vuelidate';
    import { required, minLength, maxLength } from 'vuelidate/lib/validators';
    import { mapState } from 'vuex';

    export default {
        name: "Login",
        mixins: [validationMixin],
        validations: {
            enteredUser: { required, minLength: minLength(4) },
            enteredPass: { required, minLength: minLength(6), maxLength: maxLength(32) },
        },
        data: () => ({
            enteredUser: null,
            enteredPass: null,
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
            }
        },
    }
</script>

<style scoped>

</style>