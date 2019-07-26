<template>
  <div class="json-editor-group">
        <div class="columns json-editor-container" v-for="editor in editors" v-bind:key="editor">
            <JsonEditor class="col-10" :jsonParams="jsonParams" :readOnly="false" @jsonUpdate="updateJsons(editor, ...arguments)"/>
            <a href="#" role="button" class="btn btn-primary btn-action btn-lg col-2 col-mx-auto" @click="removeEditor(editor)" v-if="editors.length > 1"><i class="icon icon-minus"></i></a>
        </div>
        <div class="columns">
            <div class="col-10"></div>
            <a href="#" role="button" class="btn btn-primary btn-action btn-lg col-2 col-mx-auto" @click="addEditor"><i class="icon icon-plus"></i></a>
        </div>
  </div>
</template>

<script lang="ts">
	import { Component, Vue, Prop } from 'vue-property-decorator';
    import JsonEditor from '../components/JsonEditor.vue';
    import _ from 'lodash';
	
	@Component({
		components: {
			JsonEditor
		}
	})
	export default class StratRun extends Vue {
        @Prop() jsonParams!: object;

		private editors: number[] = [];
        private jsons: any = {};

        created() {
            this.addEditor();
        }

		addEditor() {
            let nextEditor = this.editors.length == 0 ? 0 : this.editors[this.editors.length-1]+1;
            this.editors.push(nextEditor);
            this.jsons[nextEditor] = {};
		}

		removeEditor(editor) {
            const index = this.editors.indexOf(editor);
            this.editors.splice(index, 1);
            delete this.jsons[editor];
            this.$emit('jsonsUpdate', _.values(this.jsons));
		}

		updateJsons(editor, value, valid) {
            this.jsons[editor] = {value:value,valid:valid};
            this.$emit('jsonsUpdate', _.values(this.jsons));
		}
	}
</script>

<style lang="scss" scoped>
	#addEditor {
		margin-top: 15px;
	}

	.columns {
		margin: 0 !important;
	}

    .json-editor-container {
        margin-bottom: 10px !important;
    }
</style>
