<template>
	<div class="strat-run" :class="{ 'is-empty': strats.length == 0 }" v-if="strats">
		<EmptyCard v-if="strats.length == 0">
			<template v-slot:title>
				Nenhuma estratégia foi encontrada
			</template>
			<template v-slot:description>
				Tente <router-link :to="{name:'strat-create'}">criar</router-link> uma nova estratégia.
			</template>
		</EmptyCard>
		<form class="form-horizontal" v-if="strats.length > 0">
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
					<label for="stratLabel" class="form-label">Label</label>
				</div>
				<div class="col-8 col-sm-12">
					<input id="stratLabel" name="stratLabel" type="text" placeholder="My Label" v-model="stratLabel">
				</div>
			</div>
			<div v-show="selectedId" class="form-group">
				<div class="col-4 col-sm-12">
					<label class="form-label">Parâmetros</label>
				</div>
				<div class="col-8 col-sm-12">
					<JsonEditorGroup :jsonParams="stratParams" :readOnly="false" @jsonsUpdate="updateJsons"/>
				</div>
			</div>
			<div v-show="selectedId" class="form-group">
				<div class="col-ml-auto col-8 col-sm-12">
					<input type="button" value="Iniciar" class="btn btn-primary" @click="onSubmit" v-bind:class="{disabled: startingStrat}">
				</div>
			</div>
		</form>
	</div>
	<div class="loading loading-xlg" v-else></div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
    import EmptyCard from '@/components/EmptyCard.vue';
	import BetterCast from '../helpers/betterCast';
	import JsonEditorGroup from '@/components/JsonEditorGroup.vue';
	import axios from 'axios';

	@Component({
		components: {
            EmptyCard,
			JsonEditorGroup
		}
	})
	export default class StratRun extends Vue {
		private strats: any[] | null = null
		private selectedId: any = null;
		private selectedStrat: any = null;
		private stratLabel: any = '';
		private startingStrat: boolean = false;

		private stratParams: any = {};
		private jsons: any[] = [];

		async created() {
			this.strats = (await axios.get('/api/strat/list')).data;
		}

		onStratSelect() {
			this.selectedStrat = this.strats!.reduce((r,e) => e.id == this.selectedId ? e : r, null);
			this.stratParams = this.selectedStrat.params;
		}

		updateJsons(jsons) {
			this.jsons = jsons;
		}

		async onSubmit() {
			let stratParamsValues = this.jsons.map(e => e.value);
			let isValidParams = this.jsons.reduce((r,e) => r && e.valid, true);
			if (isValidParams && this.stratLabel != '') {
				this.startingStrat = true;
				try {
					let data = {
						'strat_id': this.selectedId,
						'label': this.stratLabel,
						'params': stratParamsValues
					};
					let status = (await axios.post('/api/strat/run', data)).data;
					this.$toasted.show('Estratégia iniciada!').goAway(2000)
					this.$router.push({ name: 'process' })
				}
				catch (error) {
					this.$toasted.show('Erro ao executar estratégia!', {
						type: 'error'
					}).goAway(2000);
				}
				this.startingStrat = false;
			}
			else {
				this.$toasted.show('Estratégia inválida!').goAway(2000)
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
