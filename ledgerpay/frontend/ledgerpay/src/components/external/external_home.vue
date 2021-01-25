<template lang="html">
    <div>
        This is external_home.vue
    </div>
</template>

<script>

    import { api_endpoints, helpers }from '@/utils/hooks'
    import FormSection from "@/components/forms/section_toggle.vue"
    import 'bootstrap/dist/css/bootstrap.css';
    import 'eonasdan-bootstrap-datetimepicker';

    export default {
        name: 'LedgerPayForm',
        props:{
        },
        data:function () {
            let vm = this;
            return {
            }
        },
        components: {
        },
        watch: {
        },
        computed: {
            csrf_token: function() {
              return helpers.getCookie('csrftoken')
            },
        },
        methods:{
            addEventListeners: function() {
            },
        },
        mounted: function() {
        },
        created: function() {
        },
    }
</script>

<style lang="css">

</style>

