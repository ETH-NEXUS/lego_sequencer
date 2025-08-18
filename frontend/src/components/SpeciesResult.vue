<template>
  <div class="card species-item" style="width: 18rem;">
    <img class="card-img-top" :src="species_url" v-if="species_url" :alt="species">
    <div v-else class="card-img-top loading-img">
      <fa-icon v-if="loading" icon="circle-notch" size="6x" spin />
      <fa-icon v-else-if="error" icon="question" size="6x" />
    </div>

    <div class="card-body">
      <h5 class="card-title">{{ species }}</h5>
      <p class="card-text">{{ $t('species_result.score') }}: {{ score }}</p>
      <a href="#" @click.stop="show_details" class="btn btn-primary">{{ $t('species_result.details') }}</a>&nbsp;
      <a :href="gsearch_url" target="_blank" class="btn btn-success">{{ $t('species_result.search') }} <fa-icon icon="external-link-alt" /></a>
    </div>
  </div>
</template>

<script>
export default {
    name: "SpeciesResult",
    props: {
        species: { type: String, required: true },
        score:   { type: Number, required: true },
        payload: { type: Object, required: true }
    },
    data() {
        return {
            species_url: null,
            loading: false,
            error: null
        }
    },
    computed: {
        gsearch_url() {
            return `https://www.google.com/search?safe=active&q=%22${this.species}%22`;
        }
    },
    mounted() {
        // fire off a request to our API for the image
        this.loading = true;
        fetch(`http://localhost:5000/api/species_img?species=${this.species}`)
            .then(result => result.json())
            .then(data => {
                this.loading = false;

                if (data.results.length > 0) {
                    this.species_url = data.results[0];
                }
                else {
                    throw {'error': 'no result found'};
                }
            })
            .catch((err) => {
                this.loading= false;
                this.error = err;
            });
    },
    methods: {
        show_details() {
            this.$emit('show-details', {
                title: this.species,
                img_url: this.species_url,
                score: this.score,
                payload: this.payload
            });
        }
    }
}
</script>

<style scoped>
.card-img-top {
  object-fit: cover;
  max-height: 200px;
}
.card-body {
  text-align: left;
}
.loading-img {
  background-color: #555;
  height: 200px;
  color: #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>