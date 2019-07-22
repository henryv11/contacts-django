<template>
  <div>
    <b-navbar variant="faded" type="light" class="border rounded mt-2 px-2 py-1 bg-light">
      <b-navbar-brand tag="h1" class="mb-0">
        <b-button variant="link text-dark" size="lg" class="p-0" style="text-decoration: none">
          <font-awesome-icon icon="address-book" class="mr-2" />Kontaktid
        </b-button>
      </b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <b-button variant="link text-dark" size="sm" class @click="toggleNewUser">
          <font-awesome-icon icon="user-plus" class></font-awesome-icon>
        </b-button>
        <b-nav-item-dropdown right toggle-class="text-decoration-none" no-caret>
          <template slot="button-content">
            <font-awesome-icon icon="user-cog" size="sm" style="color: black" />
          </template>
          <b-dropdown-text class="text-center">
            <p class="small text-muted m-0">{{username}}</p>
          </b-dropdown-text>
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-text>
            <b-button block variant="outline-primary" size="sm" @click="logout" class="p-1">
              <font-awesome-icon icon="sign-out-alt" rotation="180" />
              <p class="d-inline-block mb-0 ml-2">Välju</p>
            </b-button>
          </b-dropdown-text>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: "Navbar",
  data() {
    return {
      username: ""
    };
  },
  methods: {
    logout() {
      this.$store.dispatch("logout").then(() => this.$router.push("/"));
    },
    getUserName() {
      this.username = this.$store.getters.username;
      if (this.username == undefined) {
        this.$store
          .dispatch("userInfo")
          .then(() => (this.username = this.$store.getters.username));
      }
    },
    toggleNewUser() {
      this.$emit("toggleNewUser");
    }
  },
  mounted() {
    this.getUserName();
  }
};
</script>
