<template>
	<div class="strat-create">
		<form class="form-horizontal">
			<div class="form-group">
				<div class="col-4 col-sm-12">
					<label for="stratName" class="form-label">Nome da Estratégia</label>
				</div>
				<div class="col-8 col-sm-12">
					<input type="text" id="stratName" name="stratName" class="form-input" placeholder="My Strategy">
				</div>
			</div>
			<div class="form-group">
				<div class="col-4 col-sm-12">
					<label for="entryPath" class="form-label">Arquivo de Entrada</label>
				</div>
				<div class="col-8 col-sm-12">
					<input type="text" id="entryPath" name="entryPath" class="form-input" placeholder="start.py">
				</div>
			</div>
			<div class="form-group">
				<div class="col-4 col-sm-12">
					<label for="stratParams" class="form-label">Parâmetros</label>
				</div>
				<div class="col-8 col-sm-12">
					<div id="stratParams" class="jsoneditor"></div>
				</div>
			</div>
			<div class="form-group">
				<div class="col-4 col-sm-12">
					<label for="stratParams" class="form-label">Arquivo (zip) da Estratégia</label>
				</div>
				<div class="col-8 col-sm-12 text-left">
					<label for="stratFile" class="btn">Escolher Arquivo</label>
					<span id="fileName">{{ fileName }}</span>
					<input @change="onUpload" type="file" id="stratFile" name="stratFile" accept=".zip,.rar,.7zip" class="d-none"> 
				</div>
			</div>
			<div class="form-group">
				<div class="col-ml-auto col-8 col-sm-12">
					<input @click="onSubmit" type="button" value="Enviar" class="btn btn-primary">
				</div>
			</div>
		</form>
	</div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import axios from 'axios';
	import JSONEditor, { JSONEditorOptions, JSONEditorMode} from 'jsoneditor';
	import _ from 'lodash';

	@Component({
		components: {
		// HelloWorld,
		},
	})
	export default class StratCreate extends Vue {
		private editor!: any;
		private fileName: string = '';
		
		mounted() {
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
					// 'additionalProperties': false,
					// 'required': ['id'],
					// 'properties': {
					// 	'id': {
					// 		'type': ['integer','null']
					// 	}
					// }
				},
				'onEditable': fieldData => {
					// if (_.isEqual(fieldData.path, ["id"]))
					// 	return false;
					return true;
				}
			};
			let initialData = {
				// 'id': null
			};
			this.editor = new JSONEditor(container, options, initialData);
		}

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
			let fileInput = (<HTMLInputElement>document.querySelector('#stratFile'));
			this.fileName = this.getInputFileName(fileInput);
		}

		onSubmit() {
			let formData = new FormData();
			let stratName = (<HTMLInputElement>document.querySelector('#stratName'));
			let entryPath = (<HTMLInputElement>document.querySelector('#entryPath'));
			let stratParams = this.editor.get();
			let file = (<HTMLInputElement>document.querySelector('#stratFile'));

			let isValidParams = this.editor.validateSchema(stratParams);
			let isValidFile = file && file.files && file.files.length > 0;
			
			if (isValidParams && isValidFile) {
				formData.append('strat_name', stratName.value)
				formData.append('entry_path', entryPath.value)
				formData.append('params', JSON.stringify(stratParams));
				formData.append('file', file!.files![0]);
				axios.post('/api/strat/upload', formData, {
					headers: {
						'Content-Type': 'multipart/form-data'
					}
				});
			}
			else {
				alert("Dados inválidos!");
			}
		}
	}
</script>

<style lang="scss" scoped>
	@import '~jsoneditor/dist/jsoneditor.min.css';

	.form-group {
		margin-bottom: 20px;
	}

	.jsoneditor {
		min-height: 150px;
	}

	#fileName {
		vertical-align: middle;
		margin-left: 10px;
	}
</style>
