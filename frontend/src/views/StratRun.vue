<template>
  <div class="strat-run">
		<form class="form-horizontal">
			<div class="form-group">
				<div class="col-4 col-sm-12">
					<label for="stratSelect" class="form-label">Estratégia</label>
				</div>
				<div class="col-8 col-sm-12">
					<select id="stratSelect" name="stratSelect" v-model="selectedId" @change="onStratSelect">
						<option v-for="strat in strats" :value="strat.id" :key="strat.id">
							{{ strat.name }}
						</option>
					</select>
				</div>
			</div>
			<div v-show="selectedId" class="form-group">
				<div class="col-4 col-sm-12">
					<label for="stratParams" class="form-label">Parâmetros</label>
				</div>
				<div class="col-8 col-sm-12">
					<div id="stratParams" class="jsoneditor"></div>
				</div>
			</div>
			<div v-show="selectedId" class="form-group">
				<div class="col-ml-auto col-8 col-sm-12">
					<input @click="onSubmit" type="button" value="Iniciar" class="btn btn-primary">
				</div>
			</div>
		</form>
		<!-- <vue-form-generator :model="selectedStrat ? selectedStrat.params : null" :schema="schema" :formOptions="formOptions"></vue-form-generator> -->
  </div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import axios from 'axios';
	// import VueFormGenerator from "vue-form-generator";
	// import "vue-form-generator/dist/vfg.css";
	import JSONEditor, { JSONEditorOptions, JSONEditorMode} from 'jsoneditor';

	// Vue.use(VueFormGenerator);
	@Component({})
	export default class StratRun extends Vue {
		private editor!: any;
		private strats: any[] = []
		private selectedId: any = null;
		private selectedStrat: any = null;
		// schema = {
		// 	groups: [
		// 		{
		// 			legend: 'User Details',
		// 			fields: [
		// 				{
		// 					type: 'input',//email,password,select,checkbox
		// 					inputType: 'text',
		// 					label: 'abc',
		// 					model: 'abc',
		// 					// readonly: true,
		// 					// disabled: true,
		// 					// id: 'user_name',
		// 					// placeholder: 'Your name',
		// 					// featured: true,
		// 					// required: true,
		// 					// min: 6,
		// 					// hint: 'Minimum 6 characters',
		// 					// validator: 'string',
		// 					// values: ['Javascript', 'VueJS', 'CSS3', 'HTML5'],//for select
        //         			// default: true,//for checkbox
		// 				}
		// 			]
		// 		}
		// 	]
		// };
		// formOptions = {
		// 	validateAfterLoad: true,
		// 	validateAfterChanged: true,
		// 	validateAsync: true
		// };

		async created() {
			this.strats = (await axios.get('/api/strat/list')).data;
		}

		onStratSelect() {
			this.selectedStrat = this.strats.reduce((r,e) => e.id == this.selectedId ? e : r, null);
			let params = this.selectedStrat.params;
			let schema = this.createSchemaProps(params);
console.log(schema);
			if (this.editor) this.editor.destroy();
			var container = (<HTMLElement>document.querySelector('#stratParams'));
			let options: JSONEditorOptions = {
				'mode': 'tree',
				'modes': ['code', 'text', 'tree'],
				'search': false,
				'mainMenuBar': true,
				'statusBar': true,
				'navigationBar': false,
				'schema': {
					'title': 'Parâmetros',
					'type': 'object',
					'additionalProperties': false,
					'required': Object.keys(params),
					'properties': schema
				},
				// 'onEditable': fieldData => {
				// 	// if (_.isEqual(fieldData.path, ["id"]))
				// 	// 	return false;
				// 	return true;
				// }
			};
			let initialData = params;
			this.editor = new JSONEditor(container, options, initialData);
		}

		createSchemaProps(json) {
			let schema = {}
			for (let k in json) {
				let value = json[k];
				let type = this.betterCast(value);

				schema[k] = { 'type': [type] }

				if (type == 'object') {
					schema[k]['additionalProperties'] = false;
					schema[k]['required'] = Object.keys(value);
					schema[k].properties = this.createSchemaProps(value);
				}
				else if (type == 'array') {
					schema[k]['additionalItems'] = true;
					schema[k]['items'] = {
						'type': [...new Set(value.reduce((r,e) => [...r, this.betterCast(e)], []))]
					}
				}
			}
			return schema;
		}

		async onSubmit() {
			let stratParams = this.editor.get();
			let isValidParams = this.editor.validateSchema(stratParams);
			if (isValidParams) {
				let data = {
					'strat_id': this.selectedId,
					'params': [stratParams]
				};
				let status = (await axios.post('/api/strat/run', data)).data;
			}
		}



		betterCast(value) : 'string' | 'number' | 'array' | 'function' | 'object' | 'class' | 'null' | 'undefined' | 'boolean' | 'regexp' | 'error' | 'date' | 'symbol' {
			if (this.isString(value)) {
				return 'string';
			}
			else if (this.isNumber(value)) {
				return 'number';
			}
			else if (this.isArray(value)) {
				return 'array';
			}
			else if (this.isFunction(value)) {
				return 'function';
			}
			else if (this.isObject(value)) {
				return 'object';
			}
			else if (this.isClass(value)) {
				return 'class';
			}
			else if (this.isNull(value)) {
				return 'null';
			}
			else if (this.isUndefined(value)) {
				return 'undefined';
			}
			else if (this.isBoolean(value)) {
				return 'boolean';
			}
			else if (this.isRegExp(value)) {
				return 'regexp';
			}
			else if (this.isError(value)) {
				return 'error';
			}
			else if (this.isDate(value)) {
				return 'date';
			}
			else if (this.isSymbol(value)) {
				return 'symbol';
			}
			else {
				throw 'Unexpected Type';
			}
		}
		isString (value) {
			return typeof value === 'string' || value instanceof String;
		}
		isNumber (value) {
			return typeof value === 'number' && isFinite(value);
		}
		isArray (value) {
			return value && typeof value === 'object' && value.constructor === Array;
		}
		isFunction (value) {
			return typeof value === 'function';
		}
		isObject (value) {
			return value && typeof value === 'object' && value.constructor === Object;
		}
		isClass (value) {
			return value && typeof value === 'object' && value.constructor === Function;
		}
		isNull (value) {
			return value === null;
		}		
		isUndefined (value) {
			return typeof value === 'undefined';
		}
		isBoolean (value) {
			return typeof value === 'boolean';
		}
		isRegExp (value) {
			return value && typeof value === 'object' && value.constructor === RegExp;
		}
		isError (value) {
			return value instanceof Error && typeof value.message !== 'undefined';
		}
		isDate (value) {
			return value instanceof Date;
		}
		isSymbol (value) {
			return typeof value === 'symbol';
		}
	}
</script>
