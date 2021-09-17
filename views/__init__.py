"""
view instances declarations
"""
from database.helpdesk import HelpDesk
from views.affiliates import AffiliatesView, RecruitsView
from views.apikeys import APIKeysView
from views.helpdesk import TicketView, HelpDeskView
from views.memberships import MembershipsView, MembershipPlansView, CouponsView
from views.organization import OrganizationView
from views.services import ServicesView
from views.users import UserView
from views.wallet import WalletView


affiliates_view: AffiliatesView = AffiliatesView()
recruits_view: RecruitsView = RecruitsView()
api_keys_view: APIKeysView = APIKeysView()
memberships_view: MembershipsView = MembershipsView()
membership_plans_view: MembershipPlansView = MembershipPlansView()
coupons_view: CouponsView = CouponsView()
organization_view: OrganizationView = OrganizationView()
services_view: ServicesView = ServicesView()
user_view: UserView = UserView()
wallet_view: WalletView = WalletView()
ticket_view: TicketView = TicketView()
helpdesk_view: HelpDeskView = HelpDeskView()