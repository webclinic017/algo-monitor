<template>
    <v-autocomplete class="multi-select" multiple chips
        :label="label"
        v-model="selectedItems"
        :items="items"
        @change="onSelectChange">
        <template v-slot:prepend-item>
            <v-list-item ripple @click="clearFilter">
                <v-list-item-content>
                    <v-list-item-title>Limpar</v-list-item-title>
                </v-list-item-content>
            </v-list-item>
            <v-divider class="mt-2"></v-divider>
        </template>
    </v-autocomplete>
</template>

<script lang="ts">
	import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
    
	@Component({})
	export default class MultiSelect extends Vue {
        @Prop() label!: string;
        @Prop() items!: any[];
        @Prop() selectId!: string;
        @Prop() value!: string[];
        selectedItems: string[] = [];
        
        @Watch('value')
        onValueChange(value: string[], oldValue: string[]) {
            this.selectedItems = value;
        }

        @Watch('selectedItems')
        onSelectedItemsChange(value: string[], oldValue: string[]) {
            this.$emit("input", value);
        }

        mounted() {
            let items = localStorage.getItem(this.selectId);
            if (items) this.selectedItems = JSON.parse(items);
        }

        clearFilter() {
            this.$nextTick(() => {
                this.selectedItems = [];
                localStorage.setItem(this.selectId, JSON.stringify(this.selectedItems));
            });
        }

        onSelectChange(items) {
            localStorage.setItem(this.selectId, JSON.stringify(items));
        }
    }
</script>

<style lang="scss" scoped>
    .multi-select ::v-deep {
        .v-select__selections {
            overflow-x: hidden;
            width: 100%;
            justify-content: flex-end;
            flex-wrap: nowrap;
            .v-chip.v-size--default {
                height: 28px;
            }
        }
    }
</style>