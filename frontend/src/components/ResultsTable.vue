<template>
    <vue-good-table class="vue-good-table" ref="vue-good-table" styleClass="vgt-table"
        :columns="columns"
        :rows="rows"
        :sort-options="{
            enabled: true
        }"
        :search-options="{
            enabled: search,
            placeholder: 'Pesquisar'
        }"
        :pagination-options="{
            enabled: true,
            perPage: 25,
            rowsPerPageLabel: 'Linhas por página',
            ofLabel: 'de',
        }"
        @on-sort-change="onSortChange"/>
</template>

<script lang="ts">
	import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
	import { VueGoodTable } from 'vue-good-table';
    import FlattenObject from '../helpers/flattenObject';
    import _ from 'lodash';
    import BetterCast from '../helpers/betterCast';
	
	@Component({
        components: {
            VueGoodTable
        }
    })
	export default class ResultsTable extends Vue {
        @Prop() records!: any[];
        @Prop() search!: boolean;
        private columns: any[] = [];
        private rows: any[] = [];
        private sorts: any[] = [];

        @Watch('records', {
            immediate: true,
            deep: true
        })
        onResultsChange(value: any[], oldValue: any[]) {
            this.tableSetup(value);
        }

        @Watch('sorts', {
            immediate: true,
            deep: true
        })
        onSortsChange(value: any[], oldValue: any[]) {
            this.$emit('sorts', value);
        }

        tableSetup(records) {
            if (!records || !BetterCast.isArray(records)) return
            
            let flatResults = records.map(e => {
                let { id, ...rest } = e;
				return {
                    id: id,
                    ...FlattenObject.flatten(rest, '.')
                }
            });
            
			let columns = flatResults.reduce((red,el) => {
				let currentColumns = red.map(r => r.field);
				for (let k in el) {
					if (!_.includes(currentColumns, k)) {
						red.push(
							{
								label: k,
								field: k,
								type: typeof(el[k]) == "number" ? "number" : "text"
							});
					}
				}
				return red;
            }, []);
            
            this.rows = _.cloneDeep(records);
            this.columns = columns;
            
            let idConfig = _.find(this.columns, { 'field': 'id' });
            if (idConfig) idConfig.html = true;
            for (let j in this.rows[0]['config']) {
                let labelConfig = _.find(this.columns, { 'field': `config.${j}.label` });
                if (labelConfig) labelConfig.html = true;
            }
            for (let i in this.rows) {
                this.rows[i]['id'] = `<a href="/result/id/${this.rows[i]['id']}">${this.rows[i]['id']}</a>`
                for (let j in this.rows[i]['config']) {
                    this.rows[i]['config'][j]['label'] = `<a href="/result/label/${encodeURIComponent(encodeURIComponent(encodeURIComponent(this.rows[i]['config'][j]['label'])))}">${this.rows[i]['config'][j]['label']}</a>`}
            }
        }

        onSortChange(params) {
            this.sorts = params;
        }
    }
</script>

<style lang="scss" scoped>

</style>
