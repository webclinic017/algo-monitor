<template>
    <div class="smart-table" id="scrollTo">
        <div class="filter-wrapper">
            <span class="filter-item select-wrapper">
                <MultiSelect class="columns-select" label="Filtrar Colunas" :selectId="tableId + '_table'" :items="flattenItemsKeys" v-model="selectedItems"/>
            </span>
            <span class="filter-item">
                <v-btn text icon @click="switchTableStacked">
                    <v-icon>mdi-table</v-icon>
                </v-btn>
            </span>
        </div>
        <VueFakeScroll ref="fakeScroll" class="fake-scroll" :scroll-width="tableWidth" :scroll-height="1" @update="scrollUpdate"/>
        <div class="boot-table-wrapper">
            <b-table ref="table" class="boot-table"
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
                :sort-compare-options="{ numeric: true }"
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
            v-if="numPages > 1"
            v-scroll-to="{target:'#scrollTo',offset:0}"/>
    </div>
</template>

<script lang="ts">
	import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
    import FlattenObject from '../helpers/flattenObject';
    import BetterCast from '../helpers/betterCast';
    import MultiSelect from '../components/MultiSelect.vue';
    import VScrollTo from '../directives/scroll.directive';

    import _ from 'lodash';
    import { TablePlugin } from 'bootstrap-vue';
    import VueFakeScroll from 'vue-fake-scroll';

    Vue.use(TablePlugin)
    
	@Component({
        components: {
            MultiSelect,
            VueFakeScroll
        },
        directives: {
            VScrollTo
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
        private tableWidth: number = 0;

        private scrollWatcherThrottle!: Function;
        private scrollUpdateThrottle!: Function;

        created() {
            this.scrollWatcherThrottle = _.throttle(() => this.fakeScrollElem.scrollLeft = this.tableElem.scrollLeft, 100);
            this.scrollUpdateThrottle = _.throttle(update => this.tableElem.scrollLeft = update.scrollLeft, 50);
        }

        mounted() {
            this.tableElem.addEventListener('scroll', this.scrollWatcher);
            window.addEventListener('resize', this.updateWidth);
            this.updateWidth();

            let selectedItems = localStorage.getItem(this.tableId);
            if (selectedItems)
                this.selectedItems = JSON.parse(selectedItems);
            
            let tableStacked = localStorage.getItem(this.tableId + '_stacked');
            if (tableStacked)
                this.tableStacked = JSON.parse(tableStacked);
        }

        unmounted() {
            this.tableElem.removeEventListener('scroll', this.scrollWatcher);
            window.removeEventListener('resize', this.updateWidth);
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

        @Watch('selectedItems')
        onSelectChange() {
            console.log(123);
            this.updateWidth();
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
            return this.fields.map(e => {return { 'key': e, 'label': e, 'sortable': true }});
        }

        get fakeScrollElem() {
            return (<HTMLElement>(<any>this.$refs.fakeScroll).$el);
        }

        get tableElem() {
            return (<HTMLElement>(<any>this.$refs.table).$el);
        }

        clearFilter() {
            this.$nextTick(() => {
                this.selectedItems = [];
                localStorage.setItem(this.tableId, JSON.stringify(this.selectedItems));
            });
        }

        // isLabel(txt) {
        //     return txt.match(/^config.*label$/) != null;
        // }

        encodeUri(label) {
            return encodeURIComponent(label);
        }

        switchTableStacked() {
            this.tableStacked = !this.tableStacked;
            localStorage.setItem(this.tableId + '_stacked', JSON.stringify(this.tableStacked));
        }

        updateWidth() {
            this.$nextTick(() => {
                this.tableWidth = this.tableElem.scrollWidth;
                if (this.tableElem.scrollWidth == this.tableElem.offsetWidth) {
                    this.fakeScrollElem.style.display = 'none';
                }
                else {
                    this.fakeScrollElem.style.display = '';
                }
            });
        }

        scrollWatcher() {
            this.scrollWatcherThrottle();
        }

        scrollUpdate(update) {
            this.scrollUpdateThrottle(update);
        }
    }
</script>

<style lang="scss" scoped>
    .smart-table .boot-table-wrapper ::v-deep  {
        @import '@/assets/bootstrap-vue.scss';
        @import 'node_modules/bootstrap/scss/tables';
        @import 'node_modules/bootstrap-vue/src/components/table';
        .table {
            color: inherit;
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
            tr:hover {
                color: inherit !important;
            }
            &.b-table-stacked > tbody > tr > :first-child {
                border-top-width: 10px !important;
            }
        }
    }

    .filter-wrapper {
        .filter-item {
            display: inline-block;
            &.select-wrapper {
                width: 100%;
                max-width: 300px;
                @media (max-width: 600px) {
                    max-width: none;
                }
                .columns-select {
                    width: 100%;
                }
            }
        }
    }

    .fake-scroll ::v-deep {
        .resize-observer {
            height: 1px;
        }

        @media (max-width: 600px), (hover: none) {
            display: none;
        }
    }
</style>