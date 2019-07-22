<template>
  <div class="strat-run">
	  	<select v-model="selectedId" @change="onStratSelect">
			<option v-for="strat in strats" :value="strat.id" :key="strat.id">
				{{ strat.name }}
			</option>
		</select>
		<vue-form-generator :model="selectedStrat ? selectedStrat.params : null" :schema="schema" :formOptions="formOptions"></vue-form-generator>
  </div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import axios from 'axios';
	import VueFormGenerator from "vue-form-generator";
	import "vue-form-generator/dist/vfg.css";

	Vue.use(VueFormGenerator);
	@Component({})
	export default class StratRun extends Vue {
		strats: any[] = []
		selectedId: any = null;
		selectedStrat: any = null;
		schema = {
			groups: [
				{
					legend: 'User Details',
					fields: [
						{
							type: 'input',//email,password,select,checkbox
							inputType: 'text',
							label: 'abc',
							model: 'abc',
							// readonly: true,
							// disabled: true,
							// id: 'user_name',
							// placeholder: 'Your name',
							// featured: true,
							// required: true,
							// min: 6,
							// hint: 'Minimum 6 characters',
							// validator: 'string',
							// values: ['Javascript', 'VueJS', 'CSS3', 'HTML5'],//for select
                			// default: true,//for checkbox
						}
					]
				}
			]
		};
		formOptions = {
			validateAfterLoad: true,
			validateAfterChanged: true,
			validateAsync: true
		};

		async created() {
			this.strats = (await axios.get('/api/strat/list')).data;
		}

		onStratSelect() {
			this.selectedStrat = this.strats.reduce((r,e) => e.id == this.selectedId ? e : r, null);
			let params = this.selectedStrat.params;
			console.log(params);
			for (let p in params) {
				console.log(p);
				console.log(typeof params[p]);
				// TODO: Fazer type check do parametro e criar novo schema baseado nos tipos
				// ou utilizar jsoneditor
			}
		}
	}
</script>
