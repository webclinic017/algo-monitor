<template>
  	<div ref="editor" class="json-editor"></div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import JSONEditor, { JSONEditorOptions, JSONEditorMode } from 'jsoneditor';
	
	@Component({})
	export default class JsonEditorSimple extends Vue {
		private editor!: any;

		mounted() {
            var container = (<HTMLElement>this.$refs['editor']);
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
                'onChange': () => {
                    try {
                        let json = this.editor.get();
                        let valid = this.editor.validateSchema(json);
                        this.$emit('jsonUpdate', json, valid);
                    }
                    catch {
                        this.$emit('jsonUpdate', null, false);
                    }
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
    }
</script>

<style lang="scss" scoped>

</style>
