<template>
  <div>
    <div v-if="registrationSuccess">
      <p class="lead">Registreerimine õnnestus</p>
      <p class="small mt-4 p-0 text-muted">
        Võite nüüd
        <b-link href="#" @click="registrationContinue">sisse logida</b-link>
      </p>
    </div>
    <b-form @submit="onSubmit" @reset="onReset" v-else-if="show">
      <b-form-group
        id="input-group-username"
        label="Kasutajanimi:"
        label-for="input-username"
        label-size="sm"
        label-align="left"
        label-class="p-0 m-0"
      >
        <b-form-input
          @change="formValidation"
          id="input-username"
          v-model="form.username"
          type="text"
          :state="validation.usernameOk"
          required
        ></b-form-input>
        <b-form-invalid-feedback :state="validation.usernameOk">{{validation.usernameError}}</b-form-invalid-feedback>
        <b-form-valid-feedback :state="validation.usernameOk">Kasutajanimi sobib</b-form-valid-feedback>
      </b-form-group>

      <b-form-group
        id="input-group-password"
        label="Parool:"
        label-for="input-password"
        label-size="sm"
        label-align="left"
        label-class="p-0 m-0"
      >
        <b-form-input
          @change="formValidation"
          id="input-password"
          v-model="form.password"
          type="password"
          :state="validation.passwordOk"
          required
        ></b-form-input>
        <b-form-invalid-feedback :state="validation.passwordOk">{{validation.passwordError}}</b-form-invalid-feedback>
        <b-form-valid-feedback :state="validation.passwordOk">Parool sobib</b-form-valid-feedback>
      </b-form-group>

      <b-form-group
        id="input-group-password-confirm"
        label="Kinnita parool:"
        label-for="input-password-confirm"
        label-size="sm"
        label-align="left"
        label-class="p-0 m-0"
      >
        <b-form-input
          @change="formValidation"
          id="input-password-confirm"
          v-model="form.passwordConfirm"
          type="password"
          :state="validation.passwordConfirmOk"
          required
        ></b-form-input>
        <b-form-invalid-feedback
          :state="validation.passwordConfirmOk"
        >{{validation.passwordConfirmError}}</b-form-invalid-feedback>
        <!--<b-form-valid-feedback :state="validation.passwordConfirmOk">Looks Good.</b-form-valid-feedback>!-->
      </b-form-group>

      <b-button type="submit" :disabled="!formOk" size="sm" variant="primary">
        <b-spinner v-if="authStatus == 'loading'" small></b-spinner>
        <span v-else>Registreeri</span>
      </b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: "LoginForm",
  data() {
    return {
      form: {
        username: "",
        password: "",
        passwordConfirm: ""
      },
      validation: {
        usernameOk: null,
        usernameError: "",
        passwordOk: null,
        passwordError: "",
        passwordConfirmOk: null,
        passwordConfirmError: ""
      },
      registrationSuccess: false,
      show: true
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.formValidation();
      if (this.formOk) {
        this.$store
          .dispatch("register", this.form)
          .then(() => {
            this.registrationSuccess = true;
            this.$emit("registrationSuccess");
          })
          .catch(err => {
            this.registrationSuccess = false;
          });
      }
    },
    onReset(evt) {
      evt.preventDefault();
      this.form.username = "";
      this.form.password = "";
      this.form.passwordConfirm = "";
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    formValidation() {
      if (this.form.username.length == 0) {
        this.validation.usernameError = "";
        this.validation.usernameOk = null;
      } else if (
        this.form.username.length < 3 ||
        this.form.username.length > 15
      ) {
        this.validation.usernameError =
          "Kasutajanime pikkus peab olema 3-15 tähemärki";
        this.validation.usernameOk = false;
      } else {
        this.$http({
          url: this.$apiBaseUrl + "/api/username/availability/",
          method: "post",
          headers: {
            "Content-Type": "application/json"
          },
          data: { username: this.form.username }
        }).then(resp => {
          if (!resp.data.message) {
            this.validation.usernameError = "";
            this.validation.usernameOk = true;
          } else {
            this.validation.usernameError = "Kasutajanimi on juba võetud";
            this.validation.usernameOk = false;
          }
        });
      }

      if (this.form.password.length == 0) {
        this.validation.passwordError = "";
        this.validation.passwordOk = null;
      } else if (
        this.form.password.length < 8 ||
        this.form.password.length > 20
      ) {
        this.validation.passwordError =
          "Parooli pikkus peab olema 8-20 tähemärki";
        this.validation.passwordOk = false;
      } else {
        this.validation.passwordError = "";
        this.validation.passwordOk = true;
      }

      if (this.form.passwordConfirm.length == 0) {
        this.validation.passwordConfirmError = "";
        this.validation.passwordConfirmOk = null;
      } else if (this.form.passwordConfirm != this.form.password) {
        this.validation.passwordConfirmError =
          "Parooli kinnitus ei ühti parooliga";
        this.validation.passwordConfirmOk = false;
      } else if (this.form.passwordConfirm == this.form.password) {
        this.validation.passwordConfirmError = "";
        this.validation.passwordConfirmOk = true;
      }
    },
    registrationContinue() {
      this.$emit("registrationSuccessContinue");
      this.registrationSuccess = false;
    }
  },
  computed: {
    authStatus() {
      return this.$store.getters.authStatus;
    },
    formOk() {
      return (
        this.validation.usernameOk &&
        this.validation.passwordOk &&
        this.validation.passwordConfirmOk
      );
    }
  }
};
</script>