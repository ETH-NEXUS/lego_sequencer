<template>
  <div id="app">
    <nav class="navbar navbar-expand-md navbar-light bg-light fixed-top">
      <a class="navbar-brand" href="/">
        <img :src="require('./assets/nexus_icon.png')" alt="ETH NEXUS" class="d-inline-block align-top" height="30" />
        LEGO Sequencer v0.1
      </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarsExampleDefault">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <router-link to="/" class="nav-link" tag="a">Home</router-link>
          </li>

          <li class="nav-item">
            <router-link to="/debug" class="nav-link" tag="a">Debug</router-link>
          </li>

          <!--
          <li class="nav-item">
            <router-link to="/designer" class="nav-link" tag="a">Designer</router-link>
          </li>
          -->
        </ul>
      </div>
    </nav>

    <main role="main" class="container">
      <div class="starter-template">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script>
export default {
    name: 'app',
    components: { }
}
</script>

<style>
body {
  padding-top: 5rem;
}
.starter-template {
  text-align: left;
}

.navbar { border-bottom: solid 3px #ccc; }

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
