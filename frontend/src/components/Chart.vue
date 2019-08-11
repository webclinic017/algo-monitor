<template>
    <div class="chart">
        <MultiSelect class="chart-select" label="Selecionar Colunas" :selectId="chartId + '_chart'" :items="flattenItemsKeys" v-model="selectedItems" />
        <GChart
            type="LineChart"
            :data="chartData"
            :options="chartOptions"
            v-if="chartData.length > 0"/>
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

        get flattenItemsKeys() {
            return _.union(...this.items.map(e => Object.keys(e)));
        }

        get chartData() {
            if (this.selectedItems.length == 0) return [];

            let data = <any[]>this.items.map(e => _.pickBy(e, (value, key) => this.selectedItems.indexOf(key) > -1));
            
            let chartData: any[] = [['id']];
            data.forEach((e,i) => {
                chartData[0] = _.union(chartData[0], Object.keys(e));
                chartData[i+1] = [i+1, ...Object.values(e)];
            });

            return chartData;
        }
    }
</script>

<style lang="scss" scoped>

</style>
