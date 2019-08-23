<template>
  <div id="app">
    <nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
      <a class="navbar-brand" href="#">LEGO Sequencer v0.1</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarsExampleDefault">
        <ul class="navbar-nav mr-auto">
          <li :class="['nav-item', $route.path === '/' ? 'active' : '']">
            <a class="nav-link" href="/">Home <span v-if="$route.path === '/'" class="sr-only">(current)</span></a>
          </li>

          <li :class="['nav-item', $route.path === '/debug' ? 'active' : '']">
            <a class="nav-link" href="/debug">Debug <span v-if="$route.path === '/debug'" class="sr-only">(current)</span></a>
          </li>
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

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
  margin-top: 60px;
}

/* block styles */
.controls .btn { margin-right: 10px; }
.step { margin-bottom: 2em; }
.results { padding: 10px; border: dotted 1px #ccc; margin-top: 1em; border-radius: 3px; }
.results .error { color: darkred; }

.brick_run { display: flex; align-items: center; }
.brick_run .blaster-btn { margin-right: 10px; }

.brick_tray { display: flex; margin-bottom: 3px; }
.brick { width: 20px; height: 20px; border: solid 1px #555; margin: 2px; }
.brick_unknown { background-color: #aaa; }
.brick_black { background-color: black; }
.brick_blue { background-color: blue; }
.brick_green { background-color: green; }
.brick_yellow { background-color: yellow; }
.brick_red { background-color: red; }
.brick_white { background-color: white; }
.brick_brown { background-color: #a5512c; }
</style>
