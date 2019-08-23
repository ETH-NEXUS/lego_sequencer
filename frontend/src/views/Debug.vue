<template>
    <div>
        <h1>LEGO Sequencer (Debug)</h1>

        <div class="step">
            <h2>1. Nudge Controls</h2>
            <div class="controls">
                <button class="btn btn-sm btn-primary" @click="nudge('left')">&laquo; nudge left</button>
                <button class="btn btn-sm btn-primary" @click="nudge('right')">nudge right &raquo;</button>
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
            response: '...',
            brick_status: '(pending)',
            brick_runs: [],
            brick_error: null,
            blast_response: '...'
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
        nudge(direction) {
            fetch(`http://localhost:5000/api/nudge/${direction}`)
              .then(response => response.json())
              .then(data => {
                  this.response = data.msg;
              })
              .catch(resp => {
                  this.response = resp;
              });
        }
    }
}
</script>

<style scoped>

</style>
