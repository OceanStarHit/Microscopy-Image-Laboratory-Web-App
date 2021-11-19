import Vue from "vue";
import Tip from "../components/custom/Message";

export default function message(props) {
  const vm = new Vue({
    render(h) {
      return h(Tip, { props });
    }
  }).$mount();
  document.body.appendChild(vm.$el);
  const comp = vm.$children[0];
  comp.remove = () => {
    document.body.removeChild(vm.$el);
    vm.$destroy();
  };
  return comp;
}
