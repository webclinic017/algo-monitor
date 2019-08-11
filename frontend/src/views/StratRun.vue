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
		<v-form>
			<v-container grid-list-lg fluid>
				<v-layout wrap>
					<v-flex xs12 md6>
						<v-select
							v-model="selectedId"
							label="Estratégia"
							:items="strats"
							item-text="name"
							item-value="id"
							@change="onStratSelect"/>
					</v-flex>
					<v-flex xs12 md6 v-show="selectedId">
						<v-text-field
							v-model="stratLabel"
							label="Label"
							required
						></v-text-field>
					</v-flex>
					<v-flex xs12 v-show="selectedId">
						<label class="form-label">Parâmetros</label>
						<JsonEditorSchemaGroup
							:jsonParams="stratParams"
							:readOnly="false"
							@jsonsUpdate="updateJsons"/>
					</v-flex>
					<v-flex xs12 md4 v-show="selectedId">
						<v-btn color="primary" @click="onSubmit" :disabled="startingStrat">Iniciar</v-btn>
					</v-flex>
				</v-layout>
			</v-container>
		</v-form>
	</div>
	<div class="loading" v-else>
		<v-progress-circular indeterminate :size="100" :width="2"/>
	</div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
    import EmptyCard from '@/components/EmptyCard.vue';
	import BetterCast from '../helpers/betterCast';
	import JsonEditorSchemaGroup from '@/components/JsonEditorSchemaGroup.vue';
	import axios from 'axios';

	@Component({
		components: {
            EmptyCard,
			JsonEditorSchemaGroup
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
			this.strats = (await axios.get('/api/strat/list')).data
				.sort((a,b) => {
					if (a.name == b.name) return 0;
					else if (a.name > b.name) return 1;
					return -1;
				});
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
