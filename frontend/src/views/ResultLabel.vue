<template>
	<div class="result-label" :class="{ 'is-empty': results.length == 0 }" v-if="results">
		<EmptyCard v-if="results.length == 0">
			<template v-slot:title>
				Label não encontrada
			</template>
		</EmptyCard>
		<div class="results-wrapper" v-else>
			<Chart class="results-chart" :records="chartRecords" v-if="chartRecords.length > 0"/>
			<ResultsTable :records="results" :search="false" @sorts="sortsUpdate"/>
			<button class="btn btn-primary" @click="deleteAll" v-bind:class="{disabled: deletingResults}">Excluir Todos</button>
		</div>
	</div>
	<div class="loading loading-xlg" v-else></div>
</template>

<script lang="ts">
	import { Component, Vue, Watch } from 'vue-property-decorator';
    import EmptyCard from '@/components/EmptyCard.vue';
	import ResultsTable from '@/components/ResultsTable.vue';
	import Chart from '@/components/Chart.vue';
	import axios from 'axios';
	import _ from 'lodash';

	@Component({
		components: {
            EmptyCard,
			ResultsTable,
			Chart
		}
	})
	export default class ResultLabel extends Vue {
		private label: string | null = null;
		private results: any[] | null = null;
		private sorts: any[] = [];
		private chartRecords: any[] = [];
		private deletingResults: boolean = false;
		
		async created() {
			this.label = this.$route.params.label;
			this.results = (await axios.get(`/api/results/label/${this.label}`)).data;
		}

		sortsUpdate(sorts) {
			this.sorts = sorts;
		}
		
        @Watch("sorts", {
            immediate: true,
            deep: true
        })
        onSortsChange(value: any[], oldValud: any[]) {
			this.chartRecords = []
			
			if (!this.results || value.length == 0) return
			for (let i in value) {
				let temp = value[i]['field'].split('.').reduce((o,i)=>o[i], this.results[0]);
				if (typeof temp != "number")
					return
			}

			this.chartRecords = [['id', ..._.cloneDeep(value.map(e => e['field']))]];
			this.chartRecords = this.chartRecords.concat(this.results.reverse().reduce((r,e,i) => {
				value.forEach(f => {
					if (!r[i])
						r[i] = [i+1]
					r[i].push(f['field'].split('.').reduce((o,i)=>o[i], e));
				});
				return r;
			}, []));
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
	}
</script>

<style lang="scss">
    .result-label {
		.vgt-responsive {
			max-height: calc(100vh - 73px - 60px - 43px - 58.5px);
			overflow-y: auto;
		}
		.results-wrapper {
			&>button {
				margin-top: 7px;
			}
		}
	}

	.results-chart {
		padding-bottom: 30px;
	}
</style>