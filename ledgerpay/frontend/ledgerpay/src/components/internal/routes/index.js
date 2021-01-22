import InternalDashboard from '../dashboard.vue'
import LedgerPayAssessment from '../assessment.vue'
export default
{
    path: '/internal',
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
            component: InternalDashboard,
            name:"ledger-pay-dash"
        },
        {
            path: 'ledger_pay',
            component: {
                render(c)
                {
                    return c('router-view')
                }
            },
            children: [
                {
                    path: ':ledger_pay_id',
                    component: LedgerPayAssessment,
                    name:"ledger-pay-assessment"
                },
            ]
        },
    ]
}
