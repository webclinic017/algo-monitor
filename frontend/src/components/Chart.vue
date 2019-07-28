<template>
  <GChart
    type="LineChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script lang="ts">
    import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
    import { GChart } from 'vue-google-charts'
	
	@Component({
        components: {
            GChart
        }
    })
	export default class Chart extends Vue {
        @Prop() records!: any[];

        private chartData: any[] = [];
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

        @Watch("records", {
            immediate: true,
            deep: true
        })
        onRecordsChange(value: any[], oldValud: any[]) {
            this.chartData = value;
        }
    }
</script>

<style lang="scss" scoped>

</style>
