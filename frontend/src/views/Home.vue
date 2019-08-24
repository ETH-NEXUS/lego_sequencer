<template>
  <div>
    <Sequencer v-on:request-blast="request_blast" />
    <Blaster :sequence="active_sequence" />
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
            active_sequence: null
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