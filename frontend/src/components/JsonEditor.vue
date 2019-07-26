<template>
  <div ref="editor" class="json-editor"></div>
</template>

<script lang="ts">
	import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
	import JSONEditor, { JSONEditorOptions, JSONEditorMode} from 'jsoneditor';
    import BetterCast from '../helpers/betterCast';
	
	@Component({})
	export default class JsonEditor extends Vue {
		@Prop() jsonParams!: any;
		@Prop() readOnly!: any;
		editor!: any;

		mounted() {
			this.editorSetup(this.jsonParams);
		}

        @Watch('jsonParams', {
            immediate: false,
            deep: true
        })
        onJsonParamsChanged(value: string, oldValue: string) {
            this.editorSetup(value);
		}
		
		editorSetup(jsonParams) {
			if (this.editor) this.editor.destroy();
			let schema = this.createSchemaProps(jsonParams);
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
					'additionalProperties': false,
					'required': Object.keys(jsonParams),
					'properties': schema
                },
                'onChange': () => {
                    let json = this.editor.get();
                    let valid = this.editor.validateSchema(json);
                    this.$emit('jsonUpdate', json, valid);
                },
				'onEditable': fieldData => {
					return !this.readOnly;
				}
			};
			this.editor = new JSONEditor(container, options, jsonParams);
			
			let json = this.editor.get();
			let valid = this.editor.validateSchema(json);
			this.$emit('jsonUpdate', json, valid);
		}

        createSchemaProps(json) {
			let schema = {}
			for (let k in json) {
				let value = json[k];
				let type = BetterCast.cast(value);

				schema[k] = { 'type': [type] }

				if (type == 'object') {
					schema[k]['additionalProperties'] = false;
					schema[k]['required'] = Object.keys(value);
					schema[k].properties = this.createSchemaProps(value);
				}
				else if (type == 'array') {
					schema[k]['additionalItems'] = true;
					schema[k]['items'] = {
						'type': [...new Set(value.reduce((r,e) => [...r, BetterCast.cast(e)], []))]
					}
				}
			}
			return schema;
		}
    }
</script>

<style lang="scss" scoped>

</style>
