<template>
  <div>
    <h1>LEGO Sequencer (Debug)</h1>

    <div class="step">
      <h2>1. Nudge Controls</h2>
      <div class="controls" style="align-items: baseline;">
        <button class="btn btn-sm btn-primary" @click="nudge('left', nudge_amount)">&laquo; nudge left</button>
        <button class="btn btn-sm btn-primary" @click="nudge('right', nudge_amount)">nudge right &raquo;</button>

        <label>Bricks:
          <input type="number" name="amount" v-model="nudge_amount"/>
        </label>
      </div>

      <div class="results">
        {{ response }}
      </div>
    </div>

  </div>
</template>

<script>
export default {
    name: "Debug",
    data() {
        return {
            nudge_amount: 1,
            response: '...'
        };
    },
    methods: {
        ping() {
            fetch('http://localhost:5000/api/ping')
                .then(response => response.json())
                .then(data => {
                    this.response = data.msg;
                });
        },
        nudge(direction, nudge_amount) {
            fetch(`http://localhost:5000/api/nudge/${direction}/${nudge_amount}`)
                .then(response => response.json())
                .then(data => {
                    this.response = data.msg;
                })
                .catch(resp => {
                    this.response = resp;
                });
        },
    }
}
</script>

<style scoped>

</style>
