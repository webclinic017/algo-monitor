<template>
    <div class="smart-table">
        <div>
            <span style="display: inline-block">
                <MultiSelect class="columns-select" label="Filtrar Colunas" :selectId="tableId + '_table'" :items="flattenItemsKeys" v-model="selectedItems"/>
            </span>
            <span style="display: inline-block;">
                <v-btn text icon @click="tableStacked = !tableStacked">
                    <v-icon>mdi-table</v-icon>
                </v-btn>
            </span>
        </div>
        <div class="boot-table-wrapper">
            <b-table class="boot-table"
                :responsive="!tableStacked"
                :striped="!tableStacked"
                :hover="!tableStacked"
                :stacked="tableStacked"
                :fields="sortableFields"
                :items="flattenItems"
                :per-page="perPage"
                :current-page="page"
                :sort-by.sync="sortBy"
                :sort-desc.sync="sortDesc"
                primary-key="id">
                <template v-for="(field, index) in fields" :slot="field" slot-scope="data">
                    <!-- <div v-if="isLabel(field)" :key="index">
                        <router-link :to="{name: 'result-label', params: { label: encodeUri(data.item[field]) }}">{{ data.item[field] }}</router-link>
                    </div> -->
                    <div v-if="field == 'id'" :key="index">
                        <router-link :to="{name: 'result-id', params: { id: encodeUri(data.item[field]) }}">{{ data.item[field] }}</router-link>
                    </div>
                    <div v-else :key="index" >
                        {{ data.item[field]}}
                    </div>
                </template>
            </b-table>
        </div>
        <v-pagination class="mt-3"
            v-model="page"
            :length="numPages"
            total-visible="7"
            v-if="numPages > 1"/>
    </div>
</template>

<script lang="ts">
	import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
    import FlattenObject from '../helpers/flattenObject';
    import BetterCast from '../helpers/betterCast';
    import MultiSelect from '../components/MultiSelect.vue';

    import _ from 'lodash';
    import { TablePlugin } from 'bootstrap-vue'

    Vue.use(TablePlugin)
    
	@Component({
        components: {
            MultiSelect
        }
    })
	export default class SmartTable extends Vue {
        @Prop() items!: any[];
        @Prop() tableId!: string;

        private selectedItems: string[] = [];
        private sortBy: string = 'id';
        private sortDesc: boolean = false;
        private page: number = 1;
        private perPage: number = 10;
        private tableStacked: boolean = false;

        mounted() {
            let items = localStorage.getItem(this.tableId);
            if (items) {
                this.selectedItems = JSON.parse(items);
            }
        }

        @Watch('sortBy', {
            'immediate': true
        })
        onSortByChange() {
            this.$emit('sortedItems', this.getSortedItems());
        }

        @Watch('sortDesc', {
            'immediate': true
        })
        onSortDescChange() {
            this.$emit('sortedItems', this.getSortedItems());
        }
        
        getSortedItems() {
            return _.orderBy(this.flattenItems, [this.sortBy], [this.sortDesc ? 'desc' : 'asc']);
        }

        get numPages() {
            return Math.ceil(this.items.length / this.perPage);
        }

        get flattenItems() {
            return this.items.map(e => FlattenObject.flatten(e));
        }

        get flattenItemsKeys() {
            return _.union(...this.flattenItems.map(e => Object.keys(e)));
        }

        get fields() {
            let fields = this.selectedItems.length > 0 ? this.selectedItems : this.flattenItemsKeys;
            
            // let labels = _.filter(fields, obj => /^config.*label$/.test(obj));
            // if (labels.length > 0) {
            //     let oldValues = _.difference(fields, labels);
            //     fields = _.union(labels, oldValues);
            // }

            let index = fields.indexOf('id');
            if (index > -1) {
                let e = fields.splice(index, 1);
                fields.unshift(e[0]);
            }

            return fields;
        }

        get sortableFields() {
            return this.fields.map(e => {return { 'key': e, 'sortable': true }});
        }

        clearFilter() {
            this.$nextTick(() => {
                this.selectedItems = [];
                localStorage.setItem(this.tableId, JSON.stringify(this.selectedItems));
            });
        }

        onSelectChange(items) {
            localStorage.setItem(this.tableId, JSON.stringify(items));
        }

        // isLabel(txt) {
        //     return txt.match(/^config.*label$/) != null;
        // }

        encodeUri(label) {
            return encodeURIComponent(label);
        }
    }
</script>

<style lang="scss" scoped>
    .smart-table .boot-table-wrapper ::v-deep  {
        @import '@/assets/bootstrap-vue.scss';
        @import 'node_modules/bootstrap/scss/tables';
        @import 'node_modules/bootstrap-vue/src/components/table';
        .table {
            thead {
                th {
                    user-select: none;
                    position: relative;
                    padding-left: 24px;
                    &:before {
                        position: absolute;
                        top: 5px;
                        left: 0;
                    }
                }
            }
        }
    }
    .columns-select {
        width: 100%;
        max-width: 300px;
    }
</style>