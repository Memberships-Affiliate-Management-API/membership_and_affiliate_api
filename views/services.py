***REMOVED***
    Services View , will handle service Creation
    on the database and also on paypal, Services are necessary in order for organization
    admins to create membership payment plans,

    organizations administrators
    should host the service page on their website,

     and expose the service on the admin section of their website.
     users will be able to access any such website admin section upon registering
     and becoming a member of such a service.
***REMOVED***
from flask import jsonify, current_app
# noinspection PyProtectedMember
from _sdk._paypal.paypal import PayPalRecurring
from config.exception_handlers import handle_view_errors
from config.exceptions import InputError, error_codes, status_codes
from config.use_context import use_context
from database.services import ServiceValidator, Services


class ServicesView(ServiceValidator):
    ***REMOVED***
        this will run api endpoints for memberships services, users have to first create a service
        and then payment plans for that service in order to activate the plan
    ***REMOVED***

    def __init__(self):
        super(ServicesView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @use_context
    @handle_view_errors
    def create_service(self, organization_id: str, uid: str, name: str,
                       description: str, category: str, image_url: str,
                       home_url: str) -> tuple:
        ***REMOVED***
            :param organization_id: the organization the service belongs to
            :param uid: created_by_uid / the user creating this service
            :param name: name of the service being created
            :param description: description of the service being created
            :param category: service category
            :param image_url: if service has an image the location of the image
            :param home_url: page containing service descriptions and pricing
        :return:
        ***REMOVED***
        if not isinstance(name, str) or not bool(name.strip()):
            message: str = "Service Name cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(description, str) or not bool(description.strip()):
            message: str = "Service Description cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(category, str) or not bool(category.strip()):
            message: str = "Service Category cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if self.can_create_service(uid=uid, organization_id=organization_id) is True:
            name: str = name.strip().lower()
            description: str = description.strip().lower()
            category: str = category.strip().lower()
            services_instance: Services = Services.query(Services.name == name,
                                                         Services.organization_id == organization_id).get()

            if isinstance(services_instance, Services):
                message: str = '''a service with that name already exist in your organization 
                please use a different name'''

                return jsonify({'status': False, 'message': message}), error_codes.resource_conflict_error_code

            # TODO create service in paypal obtain service_id
            paypal_services_instance: PayPalRecurring = PayPalRecurring(app=current_app, custom_id=organization_id)
            # NOTE: Adding service descriptions to a paypal plan endpoint
            paypal_services_instance.set_service_details(name=name, description=description, category=category,
                                                         image_url=image_url, home_url=home_url)

            # NOTE: this creates the paypal service / product and returns a response
            service_response = paypal_services_instance.create_service()
            # TODO -Alternatively Use webhooks to capture the results of service creation

            if service_response.status_code == 201:
                # NOTE: Status Code or 201 mean the service was created successfully
                service_id = service_response.result.id
                services_instance: Services = Services(organization_id=organization_id, created_by_uid=uid,
                                                       service_id=service_id, name=name, description=description,
                                                       category=category, image_url=image_url, home_url=home_url)
                key = services_instance.put(retries=self._max_retries, timeout=self._max_timeout)

                message: str = '''Successfully created plan service you may proceed to 
                create payment plans for this service'''
                return jsonify({'status': False, 'message': message}), status_codes.successfully_updated_code

            message: str = '''Remote Error: Unable to create plan service please try again later or inform admin'''
            return jsonify({'status': False, 'message': message}), error_codes.remote_data_error

        message: str = '''You are not authorized to create services in this organization'''
        return jsonify({'status': False, 'message': message}), error_codes.access_forbidden_error_code

        # TODO Investigate how we can update services especially on paypal
        # TODO the steps that follows after creating a
        #   service will be integrated into memberships
