<template>
    <div>
        <FormSection :formCollapse="false" label="Payment Item" Index="payment_item">
            <template v-if="payment_items">
                <div class="form-group row">
                    <label class="col-sm-2">Payment Item</label>
                    <select class="form-control col-sm-4" v-model="payment_item_selected">
                        <option value=""></option>
                        <option v-for="payment_item in payment_items" :value="payment_item" :key="payment_item.id">
                            <span>
                                {{ payment_item.display_name }}
                            </span>
                        </option>
                    </select>
                </div>
            </template>
        </FormSection>
    </div>
</template>

<script>

    import { api_endpoints, helpers }from '@/utils/hooks'
    import FormSection from "@/components/forms/section_toggle.vue"
    import 'bootstrap/dist/css/bootstrap.css';
    import 'eonasdan-bootstrap-datetimepicker';

    export default {
        name: 'SectionPaymentItem-section-payment-item-vue',
        props:{

        },
        data:function () {
            let vm = this;
            return {
                payment_items: [],
                payment_item_selected: null,
            }
        },
        components: {
            FormSection,
        },
        watch: {

        },
        computed: {
            csrf_token: function() {
              return helpers.getCookie('csrftoken')
            },
        },
        methods:{
            fetchPaymentItems: function(){
                let vm = this;
                vm.$http.get('/api/payment_item/list_for_external').then((response) => {
                    console.log(response)
                    vm.payment_items = response.body;
                },(error) => {
                    console.log(error);
                })
            },
            addEventListeners: function() {

            },
        },
        mounted: function() {

        },
        created: function() {
            this.fetchPaymentItems()
        },
    }
</script>

<style lang="css">
    .grow1 {
        flex-grow: 1;
    }
</style>
