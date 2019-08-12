import Vue, { DirectiveOptions } from 'vue';

const VScrollTo: DirectiveOptions = {
    bind(el, binding, vnode) {
        const value = binding.value;
        if (el && typeof(value) === 'object' &&
            'target' in value &&
            'offset' in value &&
            value.target.match(/^#/) != null) {
            el.addEventListener('click', () => window.scrollTo(0,document.querySelector(value.target).offsetTop + value.offset));
        }
    }
};

export default VScrollTo;
Vue.directive('scroll-to', VScrollTo)