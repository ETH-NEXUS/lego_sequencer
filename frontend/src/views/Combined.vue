<template>
  <div>
    <div>
      <h2>Scan Sequence</h2>

      <Sequencer v-on:request-blast="request_blast" />
    </div>

    <div>
      <h2>BLAST Results</h2>

      <Blaster :sequence="active_sequence" />
    </div>
  </div>
</template>

<script>
import Sequencer from "../components/Sequencer";
import Blaster from "../components/Blaster";

export default {
    name: "Home",
    components: {Blaster, Sequencer},
    data() {
        return {
            active_sequence: null,
            username: ""
        }
    },
    methods: {
        request_blast(sequence) {
            console.log("BLAST requested: ", sequence);
            this.active_sequence = sequence;
        }
    }
}
</script>

<style scoped>

</style>