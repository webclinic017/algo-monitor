<template>
    <div class="chart">
        <MultiSelect class="chart-select" label="Selecionar Colunas" :selectId="chartId + '_chart'" :items="flattenItemsKeys" v-model="selectedItems" />
        <div v-if="chartData.length > 0">
            <GChart
                type="LineChart"
                :data="chartData"
                :options="chartOptions"
                v-if="resize"/>
        </div>
        <div v-else>
            Nenhuma coluna selecionada
        </div>
    </div>
</template>

<script lang="ts">
    import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
    import { GChart } from 'vue-google-charts'
    import FlattenObject from '../helpers/flattenObject';
    import MultiSelect from '../components/MultiSelect.vue';

	import _ from 'lodash';
    import BetterCast from '../helpers/betterCast';
	
	@Component({
        components: {
            GChart,
            MultiSelect
        }
    })
	export default class Chart extends Vue {
        @Prop() items!: any[];
        @Prop() chartId!: string;
        selectedItems: string[] = [];
        resize: boolean = true;

        chartOptions: object = {
            // title: 'Resultados',
            // subtitle: 'Sales, Expenses, and Profit: 2014-2017',
            // width: 400,
            legend: {
                position: 'top',
                maxLines: 2
            },
            height: 400,
            hAxis: {
                title: 'Índice do Resultado'
            },
            chartArea: {
                left: 50,
                width: '95%',
                height: '65%'
            }
        }

        mounted() {
            window.addEventListener('resize', this.resizeHandler);
        }

        unmounted() {
            window.removeEventListener('resize', this.resizeHandler);
        }

        get flattenItemsKeys() {
            return _.union(...this.items.map(e => {
                let validColumns: string[] = [];
                for (let k in e)
                    if (BetterCast.isNumber(e[k])) validColumns.push(k);
                return validColumns;
            }));
        }

        get chartData() {
            if (this.selectedItems.length == 0) return [];
            let data = <any[]>this.items.map(e => _.pickBy(e, (value, key) => this.selectedItems.indexOf(key) > -1));
            let chartData = this.objectArrayToGoogleChartGrid(data, this.selectedItems);
            return chartData;
        }

        resizeHandler() {
            this.resize = false;
            let resizeFunc = () => this.resize = true;
            setTimeout(resizeFunc.bind(this),500);
        }

        objectArrayToGoogleChartGrid(obj: object[], allKeys: string[]) {
            var obj2 = {}
            for (let e of obj) {
                for (let k of allKeys) {
                    if (!(k in obj2)) obj2[k] = [];
                    if (k in e) obj2[k].push(e[k])
                    else obj2[k].push(null)
                }
            }

            var obj3 = [["id"]];
            Object.keys(obj2).forEach((e,i) => {
                obj3[0].push(e);
                obj2[e].forEach((e2,i2) => {
                    if (obj3[i2+1] == undefined) obj3[i2+1] = [i2+1]
                    obj3[i2+1][i+1] = e2
                });
            });

            // var obj4 = obj3.filter(e => e.slice(1).reduce((r,v) => r || v != null, false));

            return obj3;
        }
    }
</script>

<style lang="scss" scoped>
    .chart-loading {
        display: block;
        margin: 0 auto;
    }
</style>
