<template>
    <v-container class="json-editor-group" grid-list-lg fluid>
        <v-layout wrap>
            <v-flex xs12>
                <div class="json-editor-container" v-for="editor in editors" v-bind:key="editor">
                    <v-layout wrap>
                        <v-flex xs10>
                        <JsonEditorSchema :jsonParams="jsonParams" :readOnly="false" @jsonUpdate="updateJsons(editor, ...arguments)"/>
                        </v-flex>
                        <v-flex xs2 text-center align-self-center>
                            <v-btn color="primary" text icon @click="removeEditor(editor)" v-if="editors.length > 1">
                                <v-icon>mdi-minus</v-icon>
                            </v-btn>
                        </v-flex>
                    </v-layout>
                </div>
            </v-flex>
            <v-flex xs2 offset-xs10 text-center align-self-center>
                <v-btn color="primary" text icon @click="addEditor">
                    <v-icon>mdi-plus</v-icon>
                </v-btn>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script lang="ts">
	import { Component, Vue, Prop } from 'vue-property-decorator';
    import JsonEditorSchema from '../components/JsonEditorSchema.vue';
    import _ from 'lodash';
	
	@Component({
		components: {
			JsonEditorSchema
		}
	})
	export default class JsonEditorSchemaSchemaGroup extends Vue {
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

	.container {
        padding-left: 0;
        padding-right: 0;
	}

    .json-editor-container {
        margin-bottom: 10px !important;
    }
</style>
