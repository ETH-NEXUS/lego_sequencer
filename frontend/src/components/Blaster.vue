<template>
  <div class="step">
    <h2>2. BLAST Results</h2>

    <div v-if="sequence" class="sequence_tray list-group-item">
        <span><b>Sequence:</b> {{ sequence }}</span>
        <button class="btn btn-primary" @click="blast_sequence(sequence)" :disabled="blast_pending">Run BLAST</button>
    </div>

    <div class="container-fluid" v-if="blast_status || blast_hits">
      <div class="row">
        <div class="col md-6 status_pane">
          <h5>Status:</h5>
          <ol>
            <li v-for="(rec, idx) in blast_status">
              {{ rec.status }}
              <fa-icon v-if="blast_pending && idx === blast_status.length - 1" icon="spinner" pulse />
            </li>
          </ol>
        </div>

        <div class="col md-6 results_pane">
          <div v-if="blast_result">
            <h5>Hits:</h5>
            <ul>
              <li v-for="hit in blast_unique_hits">
                {{ hit.sciname }} (score: {{ hit.score }})
              </li>
            </ul>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import * as oboe from 'oboe';
import uniqBy from "lodash/uniqBy";
import {col_to_base} from "../constants";

export default {
    name: "Blaster",
    props: { sequence: { type: String, required: false } },
    data() {
        return {
            blast_pending: false,
            blast_status: null,
            blast_result: null,
        };
    },
    computed: {
        blast_hits() {
            if (!this.blast_result)
                return null;

            return (
                this.blast_result.data.BlastOutput2[0].report.results.search.hits.map(hit => ({
                    sciname: hit.description[0].sciname,
                    score: hit.hsps[0].score
                }))
            )
        },
        blast_unique_hits() {
            if (!this.blast_hits)
                return null;

            return uniqBy(this.blast_hits, x => x.sciname);
        }
    },
    methods: {
        blast_sequence(bases) {
            console.log("BLASTing ", bases);

            oboe(`http://localhost:5000/api/blast?sequence=${bases}`)
                .start(() => {
                    this.blast_pending = true;
                    this.blast_result = null;
                    this.blast_status = [
                        {status: `BLASTing ${bases}...`}
                    ];
                })
                .node('!.{status}', rec => {
                    console.log(rec);
                    this.blast_status.push(rec)
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
                })
                .fail(err => {
                    this.blast_status.push(err)
                })
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
  padding: 10px;
}
.status_pane {
  border: solid 1px #ccc; border-radius: 5px;
}

</style>