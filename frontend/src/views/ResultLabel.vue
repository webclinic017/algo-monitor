<template>
	<div class="result-label" :class="{ 'is-empty': results.length == 0 }" v-if="results">
		<EmptyCard v-if="results.length == 0">
			<template v-slot:title>
				Label não encontrada
			</template>
		</EmptyCard>
		<div class="results-wrapper" v-else>
			<v-expansion-panels class="mb-8">
				<v-expansion-panel>
					<v-expansion-panel-header>Gráfico</v-expansion-panel-header>
					<v-expansion-panel-content>
						<Chart class="results-chart" :items="sortedItems" :chartId="label"/>
					</v-expansion-panel-content>
				</v-expansion-panel>
			</v-expansion-panels>
			<SmartTable :items="results" :tableId="label" @sortedItems="sortedItemsUpdate"/>
			<v-btn color="error mt-7" @click="deleteAll" :disabled="deletingResults">Excluir Todos</v-btn>
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
		private label: string | null = null;
		private results: any[] | null = null;
		private deletingResults: boolean = false;
		private sortedItems: string[] = [];
		
		async created() {
			this.label = this.$route.params.label;
			this.results = (await axios.get(`/api/results/label/${this.label}`)).data;
		}
		
		async deleteAll() {
			this.deletingResults = true;
            try {
                let success = await axios.post('/api/results/delete/all', {'label': this.label}).then(r => r.data);
				this.$toasted.show('Resultados excluídos!').goAway(2000);
				this.$router.push({name: 'results'});
            } catch (error) {
				this.$toasted.show('Erro ao excluir resultados!', {
					type: 'error'
				}).goAway(2000);
            }
			this.deletingResults = false;
		}

		sortedItemsUpdate(items) {
			this.sortedItems = items;
		}
	}
</script>

<style lang="scss">
	.results-chart {
		padding-bottom: 30px;
	}

	.chart-select {
        width: 100%;
        max-width: 300px;
	}
</style>