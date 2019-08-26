<template>
  <div class="step">
    <div class="controls">
      <button class="btn btn-primary" @click="scan_bricks" :disabled="active_read">scan bricks</button>
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
      <li v-for="(run, idx) in brick_runs" :key="run.name" :class="`list-group-item brick_run ${run.name == selected_run ? 'selected' : ''}`">
        <div class="seq_brick_tray">
          <button class="blaster-btn btn-sm btn btn-danger" @click="remove_sequence(run.name)">
            <fa-icon icon="trash" />
          </button>
          <button class="blaster-btn btn-sm btn btn-primary" @click="request_blast(run.name)">BLAST</button>

          <!-- <div v-for="brick in run.data" :class="`brick brick_${brick.color}`">&nbsp;</div>-->
          <img v-for="(brick, idx) in run.data" :key="idx" width="30" class="brick_img" :src="require(`../assets/legos/lego_${brick.color}.png`)" />
        </div>
      </li>

      <li v-if="active_read" class="list-group-item brick_run active_read">
        <div class="brick_tray">
          <button class="blaster-btn btn-sm btn btn-secondary" disabled>
            <fa-icon icon="trash" />
          </button>
          <button class="blaster-btn btn-sm btn btn-secondary" disabled>BLAST</button>
          <!-- <div v-for="(brick, idx) in active_read" :key="idx" :class="`brick brick_${brick.color}`">&nbsp;</div>-->
          <img v-for="(brick, idx) in active_read" :key="idx"  width="30"  class="brick_img" :src="require(`../assets/legos/lego_${brick.color}.png`)" />
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import * as oboe from 'oboe';
import {col_to_base} from "../constants";
import {generate} from "shortid";

const scan_status = {
    'PENDING': 'pending',
    'SCANNING': 'scanning...',
    'ERROR': 'error',
    'COMPLETE': 'done!'
};

export default {
    name: "Sequencer",
    data() {
        return {
            brick_status: 'PENDING',
            brick_runs: [],
            active_read: null,
            brick_error : null,
            blast_pending: false,
            scan_status,
            selected_run: null
        }
    },
    methods: {
        scan_bricks()  {
            this.brick_error = null;
            this.brick_status = 'SCANNING';

            oboe({ url: 'http://localhost:5000/api/query_ev3?streaming=true' })
                .start(() => {
                    this.active_read = [];
                })
                .node('!.*', (x) => {
                    // show partial proggress
                    this.active_read.push(x);
                })
                .done((z) => {
                    this.brick_status = 'COMPLETE';
                    this.brick_runs.push({
                        name: generate(),
                        data: z
                    });
                    this.active_read = null;
                })
                .fail((err) => {
                    // this.active_read = null;
                    this.active_read.push({'color': 'unknown'});
                    this.brick_status = 'ERROR';
                    console.warn(err);
                    this.brick_error = err.jsonBody && err.jsonBody.error ? err.jsonBody.error : err.body;
                });
        },
        remove_sequence(name) {
            if (confirm('Remove this entry?')) {
                this.brick_runs = this.brick_runs.filter(x => x.name !== name);
                if (this.selected_run === name) {
                    this.selected_run = null;
                }
            }
        },
        clear_all() {
            if (confirm('Clear all entries?')) {
                this.brick_runs = [];
                this.selected_run = null;
            }
        },
        request_blast(name) {
            const sequence = this.brick_runs.find(x => x.name === name);
            if (sequence) {
                this.selected_run = name;
                const bases = sequence.data.map(x => col_to_base[x.color]).join("");
                this.$emit('request-blast', bases);
            }
            else {
                alert(`Unable to find sequence with name ${name}!`);
            }
        }
    }
}
</script>

<style scoped>
.brick_run { display: flex; align-items: center; }
.brick_run .blaster-btn { margin-right: 10px; }

.brick_run.selected {
  background: #b5e0ff;
}

.active_read { opacity: 0.5; }

.brick_img {
  margin-right: 3px;
  background-color: #777;
  border-radius: 5px;
  padding: 5px;
  vertical-align: bottom;
}

.seq_brick_tray { display: flex; margin-bottom: 3px; width: 100%; align-items: center; }
.brick {
  background: url('../assets/four_dots_small_translucent.png') no-repeat 4px 3px;
  flex: 0 1 30px; height: 32px; border: solid 1px #555; margin: 2px; border-bottom: solid 10px #777;
}
.brick_unknown { background-color: #aaa; border-bottom-color: #555; }
.brick_black { background-color: black; border-bottom-color: #777; }
.brick_blue { background-color: #464aff; border-bottom-color: darkblue; }
.brick_green { background-color: green; border-bottom-color: darkgreen; }
.brick_yellow { background-color: yellow; border-bottom-color: #b4b400; }
.brick_red { background-color: red; border-bottom-color: darkred; }
.brick_white { background-color: white; border-bottom-color: #ccc; }
.brick_brown { background-color: #a5512c; border-bottom-color: darkred; }
</style>