<template>
  <div>
    <div v-if="sequence" class="sequence_tray list-group-item">
      <div v-for="(letter, idx) in sequence" :key="idx" class="translated_tile align-middle">
        {{ letter }}
      </div>

      <button class="btn btn-primary" @click="blast_sequence(sequence)" :disabled="blast_pending" style="white-space: nowrap;">
        <span v-if="blast_pending">
          <fa-icon icon="circle-notch" spin />
          Running BLAST...
        </span>
        <span v-else>{{ blast_result ? 'Re-run' : 'Run'}} BLAST</span>
      </button>
    </div>

    <div v-if="blast_status || blast_hits" class="status_and_results">
      <transition-group name="slideup" mode="out-in">

        <div class="status_pane" key="status_pane" v-if="!blast_result || !blast_first_five || blast_first_five.length <= 0">
          <h4>Status:</h4>

          <div class="status_scroller" ref="status_scroller">
            <transition-group name="slideright" tag="ol">
              <li v-for="(rec, idx) in blast_status" :key="idx">
                <span v-html="rec.status"></span>
                <fa-icon v-if="blast_pending && idx === blast_status.length - 1" icon="circle-notch" spin />
              </li>
            </transition-group>
            </div>
        </div>

        <div class="results_pane" key="results_pane" v-if="blast_result">
          <div>
            <h3 style="text-align: left;">Hits ({{ blast_unique_hits.length }}) (<a :href="job_url">view on NCBI</a>):</h3>
            <hr />

            <div v-if="blast_unique_hits.length > 0">
              <div class="species-tiles">
                <div class="species-tile" v-for="hit in blast_visible_unique_hits" :key="hit.sciname">
                  <SpeciesResult :species="hit.sciname" :score="hit.score" :payload="hit.payload" v-on:show-details="show_details" />
                </div>
              </div>
              <div v-if="blast_visible_hits < blast_unique_hits.length">
                <hr />
                <button class="btn btn-primary" @click="show_more_results()">Show More Results</button>
              </div>
            </div>

            <div v-else class="no-results">
              No matching species found.
              <br />
              Try again with another sequence!
            </div>
          </div>
        </div>

      </transition-group>
    </div>

    <Sidebar ref="sidedar">
      <template v-slot:default="data">
        <div v-for="(hit, idx) in data.hit.payload.hsps" class="hit-data">
          <h4 v-if="data.hit.payload.hsps.length > 1">Hit #{{ (idx+1) }}</h4>

          <div class="sec">
            <h3>Score:</h3>
            <div class="value">{{ hit.score }}</div>
          </div>

          <div class="sec">
            <h3>Query/Hit Strand:</h3>
            <div class="value">{{ hit.query_strand }} / {{ hit.hit_strand }}</div>
          </div>

          <div class="sec">
            <h3>Alignment:</h3>

            <div class="value">
              <div class="mini-sec">
                <b>Length:</b><br />{{ hit.align_len }}
              </div>

              <div class="mini-sec"><b>Bases:</b>
                <div class="alignment">{{ hit.qseq }}
                  {{ hit.midline }}
                  {{ hit.hseq }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Sidebar>
  </div>
</template>

<script>
import * as oboe from 'oboe';
import uniqBy from "lodash/uniqBy";
import countBy from "lodash/countBy";
import {col_to_base} from "../constants";
import SpeciesResult from "./SpeciesResult";
import Sidebar from "./Sidebar";

export default {
    name: "Blaster",
    components: {Sidebar, SpeciesResult},
    props: { sequence: { type: String, required: false } },
    data() {
        return {
            blast_pending: false,
            blast_status: null,
            blast_result: null,
            job_id: null,
            blast_visible_hits: 6
        };
    },
    mounted() {
        if (this.sequence) {
            this.blast_sequence(this.sequence);
        }
    },
    computed: {
        blast_hits() {
            if (!this.blast_result)
                return null;

            return (
                this.blast_result.data.BlastOutput2[0].report.results.search.hits.map(hit => ({
                    sciname: hit.description[0].sciname,
                    score: hit.hsps[0].score,
                    payload: hit
                }))
            )
        },
        blast_unique_hits() {
            if (!this.blast_hits)
                return null;

            return uniqBy(this.blast_hits, x => x.sciname);
        },
        blast_visible_unique_hits() {
            if (!this.blast_unique_hits)
                return null;
            return this.blast_unique_hits.slice(0, this.blast_visible_hits);
        },
        job_url() {
            if (!this.job_id)
                return null;
            return `https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&RID=${this.job_id}`;
        }
    },
    methods: {
        blast_sequence(bases) {
            console.log("BLASTing ", bases);

            oboe(`http://localhost:5000/api/blast?sequence=${bases}`)
                .start(() => {
                    this.blast_pending = true;
                    this.blast_result = null;
                    this.blast_visible_hits = 6;
                    this.blast_status = [
                        {status: `BLASTing ${bases}...`}
                    ];
                })
                .node('!.{status}', rec => {
                    console.log(rec);
                    this.blast_status.push(rec);

                    if (rec.job_id) {
                        this.job_id = rec.job_id
                    }

                    const status_scroller = this.$refs.status_scroller;
                    if (status_scroller) {
                        setTimeout(() => {
                          status_scroller.scrollTop = status_scroller.scrollHeight;
                        }, 10);
                    }
                })
                .node('!.{results}', rec => {
                    console.log("Done: ", rec);
                    this.blast_result = {
                        sequence: bases,
                        data: rec.results
                    };
                })
                .done(() => {
                    this.blast_pending = false;
                    this.$emit('results-displayed');
                })
                .fail(err => {
                    this.blast_status.push({'status': "Error occurred during request, terminated."});
                    this.blast_pending = false;
                })
        },
        show_details(options) {
            this.$refs.sidedar.showModal(options);
        },
        show_more_results() {
            this.blast_visible_hits += 6;
        }
    }
}
</script>

<style scoped>
.sequence_tray {
  display: flex; align-items: center;
  justify-content: space-between;
}
.sequence_tray .btn {
  margin-left: 10px;
}

.status_pane, .results_pane {
  margin-top: 1em;
  padding: 10px 10px 0 10px;
}
.status_pane {
  text-align: left;
  font-size: 20px;
  /*border: solid 1px #ccc; border-radius: 5px;*/
}
.status_pane .status_scroller {
  max-height: 6.5em;
  overflow-y: auto;
}

.species-tiles {
  display: flex; flex-wrap: wrap; justify-content: space-around;
}
.species-tile {
  margin: 10px 0 10px 0;
}

.no-results {
  background-color: #eee;
  padding: 20px;
  border-radius: 10px;
  font-size: 24px; font-style: italic;
  color: #777;
  text-align: center;
}

.sec { margin-bottom: 10px; }
.sec .value { margin-left: 10px; }
.mini-sec {
  margin-bottom: 5px;
}

.alignment {
  font-family: monospace;
  white-space: pre;
  overflow-x: scroll;
}
</style>