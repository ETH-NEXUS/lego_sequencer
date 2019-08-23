<template>
  <div>
    <h1>LEGO Sequencer</h1>

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

    <div class="step">
      <h2>2. Scanning</h2>
      <div class="controls">
        <button class="btn btn-primary" @click="scan_bricks">scan bricks</button>

        <span class="status">
          <span v-if="brick_error" class="error"><b>Error:</b> {{ brick_error }}</span>
          <span v-else>{{ brick_status }}</span>
        </span>
      </div>

      <ul class="list-group" style="margin-top: 1em;">
        <li v-for="(run, idx) in brick_runs" class="list-group-item brick_run">
          <button class="blaster-btn btn btn-danger" @click="blast_sequence(run)">BLAST</button>

          <div class="brick_tray">
            <div v-for="brick in run" :class="`brick brick_${brick.color}`">&nbsp;</div>
          </div>
        </li>
      </ul>
    </div>

    <div class="step">
      <h2>3. BLAST</h2>

      <div class="results">
        {{ blast_response }}
      </div>
    </div>
  </div>
</template>

<script>
const col_to_base = {
    'green':  'A',
    'blue':   'C',
    'red':    'T',
    'yellow': 'G'
};

export default {
    name: "Home",
    data() {
        return {
            response: '...',
            brick_status: '(pending)',
            brick_runs: [],
            brick_error : null,
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
        },
        scan_bricks()  {
            this.brick_error = null;
            this.brick_status = "scanning...";

            fetch('http://localhost:5000/api/query_ev3')
                .then(response => response.json())
                .then(data => {
                    this.brick_status = "done!";
                    this.brick_runs.push(data);
                })
                .catch(resp => {
                    this.brick_error = `${resp}`;
                })
        },
        blast_sequence(sequence) {
            const bases = sequence.map(x => col_to_base[x.color]).join("");
            console.log("BLASTing ", sequence.map(x => x.color).join(", "), ", i.e.: ", bases);

            fetch(`http://localhost:5000/api/blast?sequence=${bases}`)
                .then(response => response.json())
                .then(data => {
                    this.blast_response = data;
                })
                .catch(resp => {
                    this.blast_response = `${resp}`;
                })
        }
    }
}
</script>

<style scoped>
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
.brick_brown { background-color: brown; }
</style>
