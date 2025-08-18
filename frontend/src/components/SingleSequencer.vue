<template>
  <div>
    <div class="control_tray">
      <button class="btn btn-primary" @click="scan_bricks" :disabled="active_read && !scan_success">
        {{ scan_success ? $t('sequencer.rescan_bricks') : $t('sequencer.scan_bricks') }}
      </button>

      <div class="status">
        <span v-if="brick_error" class="error"><b>Error:</b> {{ brick_error }}</span>
        <span v-else-if="brick_status !== 'PENDING'">
            <fa-icon v-if="brick_status === 'SCANNING'" icon="circle-notch" spin />
            {{ $t('sequencer.status.' + brick_status.toLowerCase()) }}
          </span>
      </div>
    </div>

    <div class="brick_tray" v-if="active_read">
      <transition-group name="bouncy">
        <img
          v-for="(brick, idx) in active_read" :key="idx"  width="35"  class="brick_img"
          :src="require(`../assets/legos/lego_${brick.color}.png`)" :alt="`${brick.color} brick`"
        />
      </transition-group>
    </div>

    <transition-group name="slideup">
      <div key="angle-bracket" v-if="active_read && scan_success">
        <fa-icon icon="angle-double-down" size="2x" key="arrow-bit" />
      </div>

      <div class="brick_tray translation"  key="translation" v-if="active_read && scan_success">
        <div v-for="(brick, idx) in active_read" :key="idx" class="translated_tile align-middle">
          {{ col_to_base[brick.color] || '-' }}
        </div>
      </div>

      <div class="control_tray" key="blast_tray" v-if="active_read && scan_success">
        <button class="btn btn-outline-secondary" @click="copy_blast(active_read)">
          <fa-icon icon="clipboard" />
          {{ $t('sequencer.copy_sequence') }}
        </button>
        <button class="btn btn-primary" @click="request_blast(active_read)">
          {{ $t('sequencer.blast_sequence') }}
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script>
import * as oboe from 'oboe';
import {col_to_base} from "../constants";
import {generate} from "shortid";


export default {
    name: "SingleSequencer",
    props: { username: { type: String, required: false } },
    data() {
        return {
            brick_status: 'PENDING',
            brick_runs: [],
            active_read: null,
            brick_error : null,
            blast_pending: false,
            col_to_base,
            query_id: null
        }
    },
    computed: {
        scan_success() {
            return this.brick_status === 'COMPLETE';
        }
    },
    methods: {
        scan_bricks()  {
            this.brick_error = null;
            this.brick_status = 'SCANNING';

            oboe({ url: `http://localhost:5000/api/query_ev3?streaming=true&username=${this.username}` })
                .start(() => {
                    this.active_read = [];
                })
                .node('!.{color}', (x) => {
                    // show partial proggress
                    this.active_read.push(x);
                })
                .node('!.{query_id}', (x) => {
                    // record the query id so we can save blast results later
                    this.query_id = x.query_id;
                })
                .done((z) => {
                    this.brick_status = 'COMPLETE';
                })
                .fail((err) => {
                    // this.active_read = null;
                    this.active_read.push({'color': 'unknown'});
                    this.brick_status = 'ERROR';
                    console.warn(err);
                    this.brick_error = err.jsonBody && err.jsonBody.error ? err.jsonBody.error : err.body;
                });
        },
        copy_blast(sequence) {
            const bases = sequence.map(x => col_to_base[x.color]).join("");

            // create a temporary DOM element into which we'll do a copy of the current URL
            const dummy = document.createElement('input'), text = bases;
            document.body.appendChild(dummy);
            dummy.value = text;
            dummy.select();
            document.execCommand('copy');
            document.body.removeChild(dummy);

            // notify the user that the copy has occurred
            this.$bvToast.toast(`Copied ${bases} to clipboard`, {
                autoHideDelay: 2000,
                title: 'Copied Sequence',
                variant: 'info',
                toaster: 'b-toaster-top-center',
                noCloseButton: true
            });
        },
        request_blast(sequence) {
            const bases = sequence.map(x => col_to_base[x.color]).join("");
            this.$emit('request-blast', bases);
        }
    }
}
</script>

<style scoped>
.brick_run { display: flex; align-items: center; }
.brick_run .blaster-btn { margin-right: 10px; }

.status {
  margin: 10px; font-size: 24px;
  display: flex; align-items: flex-start; justify-content: center;
}

.active_read.pending { opacity: 0.5; }

.control_tray { margin-top: 20px; }
.control_tray button { margin: 0 5px; border-collapse: collapse; min-width: 150px; }
</style>