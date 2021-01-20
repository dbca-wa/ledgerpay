import LedgerPayForm from '../../ledgerpay_form.vue'
import LedgerPaySubmit from '../ledgerpay_submit.vue'
export default
{
    path: '/external',
    component:
    {
        render(c)
        {
            return c('router-view')
        }
    },
    children: [
        {
            path: '/',
            component: LedgerPayForm,
            name: 'external-ledgerpay-form'
        },
        {
            path: 'submit',
            component: LedgerPaySubmit,
            name:"submit_ledgerpay"
        },
    ]
}
