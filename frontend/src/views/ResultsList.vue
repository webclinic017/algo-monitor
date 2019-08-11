<template>
	<div class="result-list" :class="{ 'is-empty': results.length == 0 }" v-if="results">
		<EmptyCard v-if="results.length == 0"/>
		<div class="results-wrapper" v-else>
			<h2>Labels</h2>
			<v-list class="labels-list">
				<v-container fluid grid-list-lg text-center>
				<v-layout wrap>
					<v-flex xs12 md6 lg4 xl3 v-for="(label, index) in labels" :key="index" >
						<v-list-item class="label-item elevation-2" :to="{name:'result-label', params:{label:encodeUri(label)}}">
							<v-list-item-content>
								<v-list-item-title>{{ label }}</v-list-item-title>
							</v-list-item-content>
						</v-list-item>
					</v-flex>
				</v-layout>
				</v-container>
			</v-list>
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

	import axios from 'axios';
	import _ from 'lodash';

	@Component({
		components: {
			EmptyCard,
			SmartTable
			// ResultsTable
		}
	})
	export default class ResultsList extends Vue {
		private results: any[] | null = null;
		private labels: string[] = [];

		async created() {
			this.results = (await axios.get('/api/results')).data;
			this.labels = _.union(...this.results!.map(e => e.config.reduce((r,v) => r.concat(v.label), [])));
		}

		encodeUri(txt) {
			return encodeURIComponent(txt);
		}
	}
</script>

<style lang="scss">
	.labels-list {
		background: transparent !important;
		.container {
			padding: 0;
			.label-item {
				margin: 10px 0;
				&:first-child {
					margin-top: 0;
				}
				&:last-child {
					margin-bottom: 0;
				}
			}
		}
	}
</style>
