import Vue from 'vue';

const VSort = function (value) {
    return value.sort();
}

export default VSort;
Vue.filter('sort', VSort)