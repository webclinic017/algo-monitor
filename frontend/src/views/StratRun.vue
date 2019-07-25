<template>
  <div class="strat-run">
		<form class="form-horizontal">
			<div class="form-group">
				<div class="col-4 col-sm-12">
					<label for="stratSelect" class="form-label">Estratégia</label>
				</div>
				<div class="col-8 col-sm-12">
					<select id="stratSelect" name="stratSelect" class="form-select" v-model="selectedId" @change="onStratSelect">
						<option v-for="strat in strats" :value="strat.id" :key="strat.id">
							{{ strat.name }}
						</option>
					</select>
				</div>
			</div>
			<div v-show="selectedId" class="form-group">
				<div class="col-4 col-sm-12">
					<label class="form-label">Parâmetros</label>
				</div>
				<div class="col-8 col-sm-12">
					<JsonEditorGroup :jsonParams="stratParams" @jsonsUpdate="updateJsons"/>
				</div>
			</div>
			<div v-show="selectedId" class="form-group">
				<div class="col-ml-auto col-8 col-sm-12">
					<input @click="onSubmit" type="button" value="Iniciar" class="btn btn-primary">
				</div>
			</div>
		</form>
  </div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import axios from 'axios';
	import BetterCast from '../helpers/betterCast';
	import JsonEditorGroup from '../components/JsonEditorGroup.vue';
	
	@Component({
		components: {
			JsonEditorGroup
		}
	})
	export default class StratRun extends Vue {
		private strats: any[] = []
		private selectedId: any = null;
		private selectedStrat: any = null;

		private stratParams: any = {};
		private jsons: any[] = [];

		async created() {
			this.strats = (await axios.get('/api/strat/list')).data;
		}

		onStratSelect() {
			this.selectedStrat = this.strats.reduce((r,e) => e.id == this.selectedId ? e : r, null);
			this.stratParams = this.selectedStrat.params;
		}

		updateJsons(jsons) {
			this.jsons = jsons;
		}

		async onSubmit() {
			let stratParamsValues = this.jsons.map(e => e.value);
			let isValidParams = this.jsons.reduce((r,e) => r && e.valid, true);
			if (isValidParams) {
				let data = {
					'strat_id': this.selectedId,
					'params': stratParamsValues
				};
				let status = (await axios.post('/api/strat/run', data)).data;
			}
		}
	}
</script>

<style lang="scss" scoped>
	.form-select {
    	max-width: 10rem;
	}

	#addEditor {
		margin-top: 15px;
	}

	.columns {
		margin: 0 !important;
	}
</style>
