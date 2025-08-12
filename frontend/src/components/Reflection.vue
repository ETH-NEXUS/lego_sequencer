<template>
  <div class="reflection">
    <h3>Sequence Reflection</h3>
    <div v-if="loading">Generating reflection...</div>
    <pre>{{ reflection }}</pre>
    <button v-if="!loading" @click="generateReflection">Regenerate</button>
  </div>
  <Reflection
    v-if="blast_result && blast_result.sequence && blast_unique_hits && blast_unique_hits.length"
    :sequence="blast_result.sequence"
    :species-list="blast_unique_hits.slice(0, 6).map(hit => hit.sciname)"
    :username="username"
  />
</template>

<script>
export default {
  props: {
    sequence: { type: String, required: true },
    speciesList: { type: Array, required: true },
    username: { type: String, required: false }
  },
  data() {
    return {
      reflection: "",
      loading: false
    }
  },
  methods: {
    async generateReflection() {
      console.log("Reflection props:", {
        sequence: this.sequence,
        speciesList: this.speciesList,
        username: this.username
      });

      this.reflection = "";
      this.loading = true;
      const response = await fetch("/api/reflection", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          seq: this.sequence,
          species: this.speciesList,
          username: this.username
        })
      });
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        this.reflection += decoder.decode(value, { stream: true });
        // Yield to the event loop so Vue can update the DOM
        await this.$nextTick();
      }
      this.loading = false;
    }
  },
  mounted() {
    this.generateReflection();
  }
}
</script>

<style scoped>
.reflection {
  margin: 1em 0;
  padding: 1em;
  background: #f8f8f8;
  border-radius: 8px;
}
pre {
  white-space: pre-wrap;
  font-family: monospace;
}
</style>