<template>
	<div class="result-label" :class="{ 'is-empty': results.length == 0 }" v-if="results">
		<EmptyCard v-if="results.length == 0">
			<template v-slot:title>
				Label não encontrada
			</template>
		</EmptyCard>
		<div class="results-wrapper" v-else>
			<h3 class="label-title">{{ label }}</h3>
			<v-expansion-panels class="mb-8">
				<v-expansion-panel>
					<v-expansion-panel-header>Gráfico</v-expansion-panel-header>
					<v-expansion-panel-content>
						<Chart class="results-chart" :items="sortedItems" :chartId="label"/>
					</v-expansion-panel-content>
				</v-expansion-panel>
			</v-expansion-panels>
			<SmartTable :items="results" :tableId="label" @sortedItems="sortedItemsUpdate"/>
			<v-btn class="mt-7" color="primary" @click="downloadAll" :disabled="processing">Download</v-btn>
			<v-btn class="mt-7 ml-5" color="error" @click="deleteAll" :disabled="processing">Excluir Todos</v-btn>
		</div>
	</div>
	<div class="loading" v-else>
		<v-progress-circular indeterminate :size="100" :width="2"/>
	</div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
    import EmptyCard from '@/components/EmptyCard.vue';
	import SmartTable from '../components/SmartTable.vue';
	import Chart from '@/components/Chart.vue';

	import axios from 'axios';

	@Component({
		components: {
            EmptyCard,
			SmartTable,
			Chart
		}
	})
	export default class ResultLabel extends Vue {
		private label!: string;
		private results: any[] | null = null;
		private processing: boolean = false;
		private sortedItems: any[] = [];
		
		async created() {
			this.label = decodeURIComponent(this.$route.params.label);
			this.results = (await axios.get(`/api/results/label/${this.label}`)).data;
		}

		async downloadAll() {
			this.processing = true;
            try {
				// let success = await axios.get(`/api/results/download/label/${encodeURIComponent(this.label)}`).then(r => r.data);
				window.open(`/api/results/download/label/${this.label}`);
            } catch (error) {
				this.$toasted.show('Erro ao baixar resultados!', {
					type: 'error'
				}).goAway(2000);
            }
			this.processing = false;
		}
		
		async deleteAll() {
			this.processing = true;
            try {
                let success = await axios.post('/api/results/delete/all', {'label': this.label}).then(r => r.data);
				this.$toasted.show('Resultados excluídos!').goAway(2000);
				this.$router.push({name: 'results'});
            } catch (error) {
				this.$toasted.show('Erro ao excluir resultados!', {
					type: 'error'
				}).goAway(2000);
            }
			this.processing = false;
		}

		sortedItemsUpdate(items) {
			this.sortedItems = items;
		}
	}
</script>

<style lang="scss">
	.label-title {
		margin-bottom: 1.75rem;
	}

	.results-chart {
		padding-bottom: 30px;
	}

	.chart-select {
        width: 100%;
        max-width: 300px;
        @media (max-width: 600px) {
            max-width: none;
        }
	}
</style>