<template>
	<div class="strat-create">
		<v-form>
			<v-container grid-list-lg fluid>
				<v-layout wrap>
					<v-flex xs12 md4>
						<v-text-field
							v-model="stratName"
							label="Nome da Estratégia"
							required/>
					</v-flex>
					<v-flex xs12 md4>
						<v-textarea
							v-model="stratDescription"
							label="Descrição"
							no-resize
							rows="1"/>
					</v-flex>
					<v-flex xs12 md4>
						<v-text-field
							v-model="entryPath"
							label="Arquivo de Entrada"
							:hint="'Ex.: myFolder/test.py'"
							persistent-hint
							required/>
					</v-flex>
					<v-flex xs12>
						<label class="form-label">Parâmetros</label>
						<!-- <div id="stratParams" class="json-editor"></div> -->
						<JsonEditorSimple class="mt-3" @jsonUpdate="onJsonUpdate"/>
					</v-flex>
					<v-flex xs12>
						<v-btn color="secondary" @click="$refs.stratFile.click()">Escolher Arquivo</v-btn>
						<span class="ml-3">{{ fileName }}</span>
						<input type="file" id="stratFile" accept=".zip,.rar,.7zip" ref="stratFile" v-show="false" @change="onUpload"> 
					</v-flex>
					<v-flex class="mt-5" xs12 md4>
						<v-btn color="primary" @click="onSubmit" :disabled="savingStrat">Enviar</v-btn>
					</v-flex>
				</v-layout>
			</v-container>
		</v-form>
	</div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import axios from 'axios';
	import JsonEditorSimple from '@/components/JsonEditorSimple.vue';

	import _ from 'lodash';

	@Component({
		components: {
			JsonEditorSimple
		}
	})
	export default class StratCreate extends Vue {
		private editor!: any;
		private stratName: string = '';
		private stratDescription: string = '';
		private entryPath: string = '';
		private fileName: string = '';
		private stratParams: object | null = null;
		private savingStrat: boolean = false;

		getInputFileName(input: HTMLInputElement) {
			let fullPath = input.value;
			var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
			var filename = fullPath.substring(startIndex);
			if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
				filename = filename.substring(1);
			}
			return filename;
		}

		onUpload() {
			this.fileName = this.getInputFileName(<HTMLInputElement>this.$refs.stratFile);
		}

		onJsonUpdate(json, valid) {
			if (valid) this.stratParams = json;
			else this.stratParams = null;
		}

		async onSubmit() {
			let formData = new FormData();
			let file = <HTMLInputElement>this.$refs.stratFile;

			let isValidFile = file && file.files && file.files.length > 0;
			
			if (this.stratParams && isValidFile && this.stratName != '' && this.entryPath != '') {
				this.savingStrat = true;
				try {
					formData.append('strat_name', this.stratName)
					formData.append('strat_description', this.stratDescription)
					formData.append('entry_path', this.entryPath)
					formData.append('params', JSON.stringify(this.stratParams));
					formData.append('file', file!.files![0]);
					let success = await axios.post('/api/strat/upload', formData, {
						headers: {
							'Content-Type': 'multipart/form-data'
						}
					}).then(r => r.data);
					this.$toasted.show('Estratégia criada!').goAway(2000)
					this.$router.push({ name: 'process' })
				}
				catch (error) {
					this.$toasted.show('Erro ao criar estratégia!', {
						type: 'error'
					}).goAway(2000);
				}
				this.savingStrat = false;
			}
			else {
				this.$toasted.show('Estratégia inválida!').goAway(2000)
			}
		}
	}
</script>

<style lang="scss" scoped>
	@import '~jsoneditor/dist/jsoneditor.min.css';

	#fileName {
		vertical-align: middle;
		margin-left: 10px;
	}
</style>
