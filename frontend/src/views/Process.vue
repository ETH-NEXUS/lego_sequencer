<template>
  <div class="steps">
    <!-- TODO: create step-processing system -->
    <transition-group name="step" mode="out-in">

      <div v-if="current_step === 0" :key="0" class="step" id="step1">
        <h1>Welcome to the<br />LEGO Sequencer!</h1>
        <label for="name">Please enter your name:</label><br />
        <input type="text" id="name" v-model="name" placeholder="enter your name here" @submit="proceed()" /><br />
        <button class="btn btn-primary" :disabled="!name" @click="proceed()">Continue</button>
      </div>

      <div v-else-if="current_step === 1" :key="1" class="step" id="step2">
        <h1>Scan Bricks</h1>
        <SingleSequencer :username="name" v-on:request-blast="request_blast" />
      </div>

      <div v-else-if="current_step === 2" :key="2" class="step" id="step3">
        <h1>BLAST Sequence</h1>

        <Blaster :sequence="active_sequence" v-on:results-displayed="blast_complete" />

        <div v-if="ready_to_restart">
          <hr />
          <button class="btn btn-danger" @click="restart()">Start Over</button>
        </div>
      </div>

    </transition-group>
  </div>
</template>

<script>
import SingleSequencer from "../components/SingleSequencer";
import Blaster from "../components/Blaster";

export default {
    name: "Process",
    components: {Blaster, SingleSequencer},
    data() {
        return {
            name: '',
            current_step: 0,
            active_sequence: null,
            ready_to_restart: false
        }
    },
    methods: {
        restart() {
            // just choosing an invalid step to clear everything temporarily
            this.current_step = 99;

            // move to the top to prevent a jarring transition
            window.scroll({
                top: 0,
                left: 0,
                behavior: 'smooth'
            });

            // eventually load the initial page
            setTimeout(() => {
                this.name = '';
                this.current_step = 0;
                this.active_sequence = null;
                this.ready_to_restart = false;
            }, 300);
        },
        proceed() {
            if (this.current_step === 0) {
                // check if they have a name, allow them to proceed if so
                if (this.name) {
                    this.current_step = 1;
                }
            }
            else if (this.current_step === 1) {
                if (this.active_sequence) {
                    this.current_step = 2;
                }
            }
        },
        request_blast(sequence) {
            this.active_sequence = sequence;
            this.proceed();
        },
        blast_complete() {
            console.log("BLAST done!");
            this.ready_to_restart = true;
        }
    }
}
</script>

<style scoped>
.steps {
  text-align: center;
  position: relative;
}

.steps .step {
  position: absolute;
  left: 0; right: 0;
}

#step1 * { margin: 10px; }
#name {
  padding: 10px; border-radius: 5px; border: solid 1px #ccc; text-align: center;
  min-width: 300px;
}

.step-item {
  display: inline-block;
  margin-right: 10px;
}
.step-enter-active, .step-leave-active {
  transition: all 1s;
}
.step-enter, .step-leave-to /* .list-leave-active below version 2.1.8 */ {
  opacity: 0;
  transform: translateX(30px);
}
</style>