<template>
  <div>
    <h1>LEGO Sequencer</h1>

    <div class="step">
      <h2>1. Scan Sequence</h2>
      <div class="controls">
        <button class="btn btn-primary" @click="scan_bricks">scan bricks</button>
        <button class="btn btn-danger" @click="clear_all">clear runs</button>

        <span class="status">
          <span v-if="brick_error" class="error"><b>Error:</b> {{ brick_error }}</span>
          <span v-else>
            <fa-icon v-if="brick_status === 'SCANNING'" icon="spinner" pulse />
            {{ scan_status[brick_status] }}
          </span>
        </span>
      </div>

      <ul class="list-group" style="margin-top: 1em;">
        <li v-for="(run, idx) in brick_runs" class="list-group-item brick_run">
          <button class="blaster-btn btn-sm btn btn-danger" @click="blast_sequence(run)">BLAST</button>

          <div class="brick_tray">
            <div v-for="brick in run" :class="`brick brick_${brick.color}`">&nbsp;</div>
          </div>
        </li>

        <li v-if="active_read" class="list-group-item brick_run active_read">
          <div class="brick_tray">
            <button class="blaster-btn btn-sm btn btn-secondary" disabled @click="blast_sequence(run)">BLAST</button>
            <div v-for="brick in active_read" :class="`brick brick_${brick.color}`">&nbsp;</div>
          </div>
        </li>
      </ul>
    </div>

    <div class="step">
      <h2>2. BLAST Results</h2>

      <div class="results">
        {{ blast_response }}
      </div>
    </div>
  </div>
</template>

<script>
import {handleErrors} from "../utils";
import * as oboe from 'oboe';

const col_to_base = {
    'green':  'A',
    'blue':   'C',
    'red':    'T',
    'yellow': 'G'
};

const scan_status = {
    'PENDING': 'pending',
    'SCANNING': 'scanning...',
    'ERROR': 'error',
    'COMPLETE': 'done!'
};

export default {
    name: "Home",
    data() {
        return {
            nudge_amount: 1,
            brick_status: 'PENDING',
            brick_runs: [],
            active_read: null,
            brick_error : null,
            blast_response: '...',
            scan_status
        };
    },
    methods: {
        scan_bricks()  {
            this.brick_error = null;
            this.brick_status = 'SCANNING';
            this.active_read = [];

            oboe({ url: 'http://localhost:5000/api/query_ev3?streaming=true'})
                .node('!.*', (x) => {
                    // show partial proggress
                    this.active_read.push(x);
                })
                .done((z) => {
                    this.brick_status = 'COMPLETE';
                    this.brick_runs.push(z);
                    this.active_read = null;
                })
                .fail(() => {
                    this.active_read = null;
                    this.brick_status = 'ERROR';
                });
        },
        clear_all() {
            if (confirm('Clear all entries?')) {
                this.brick_runs = [];
            }
        },
        blast_sequence(sequence) {
            const bases = sequence.map(x => col_to_base[x.color] || '-').join("");
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
.brick_run { display: flex; align-items: baseline; }
.brick_run .blaster-btn { margin-right: 10px; }

.active_read { opacity: 0.75; }

.brick_tray { display: flex; margin-bottom: 3px; width: 100%; }
.brick { width: 15px; height: 25px; border: solid 1px #555; margin: 2px; }
.brick_unknown { background-color: #aaa; }
.brick_black { background-color: black; }
.brick_blue { background-color: blue; }
.brick_green { background-color: green; }
.brick_yellow { background-color: yellow; }
.brick_red { background-color: red; }
.brick_white { background-color: white; }
.brick_brown { background-color: #a5512c; }
</style>
