<template>
	<div class="result-list" :class="{ 'is-empty': results.length == 0 }" v-if="results">
		<EmptyCard v-if="results.length == 0"/>
		<div class="results-wrapper" v-else>
			<ResultsTable :records="results" :search="true"/>
		</div>
	</div>
	<div class="loading loading-xlg" v-else></div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
    import EmptyCard from '@/components/EmptyCard.vue';
	import ResultsTable from '@/components/ResultsTable.vue';
	import axios from 'axios';

	@Component({
		components: {
            EmptyCard,
			ResultsTable
		}
	})
	export default class ResultsList extends Vue {
		private results: any[] | null = null;

		async created() {
			this.results = (await axios.get('/api/results')).data;
		}
	}
</script>

<style lang="scss">
    .result-list .vgt-responsive {
        max-height: calc(100vh - 73px - 60px - 43px - 58.5px);
        overflow-y: auto;
    }
</style>
