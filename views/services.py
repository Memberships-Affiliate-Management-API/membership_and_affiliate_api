***REMOVED***
    ** Services View  Controller** ,
        will handle service Creation
        on the database and also on paypal, Services are necessary in order for organization
        admins to create membership payment plans,

        organizations administrators
        should host the service page on their website,

         and expose the service on the admin section of their website.
         users will be able to access any such website admin section upon registering
         and becoming a member of such a service.
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Optional
from flask import jsonify, current_app
# noinspection PyProtectedMember
from google.cloud import ndb
from _sdk._paypal.paypal import PayPalRecurring
from config.exception_handlers import handle_view_errors
from config.exceptions import InputError, error_codes, status_codes, DataServiceError
from config.use_context import use_context
from database.services import ServiceValidator, Services


class ServicesView(ServiceValidator):
    ***REMOVED***
        **Class ServicesView**

            this will run api endpoints for memberships services, users have to first create a service
            and then payment plans for that service in order to activate the plan
    ***REMOVED***

    def __init__(self):
        super(ServicesView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @use_context
    @handle_view_errors
    def create_service(self, organization_id: Optional[str], uid: Optional[str], name: Optional[str],
                       description: Optional[str], category: Optional[str], image_url: Optional[str],
                       home_url: Optional[str]) -> tuple:
        ***REMOVED***
            **create_service**
                creates a service locally and also on paypal

            **NOTE**
                Note products or services are needed in order to create payment plans

            :param organization_id: the organization the service belongs to
            :param uid: created_by_uid / the user creating this service
            :param name: name of the service being created
            :param description: description of the service being created
            :param category: service category
            :param image_url: if service has an image the location of the image
            :param home_url: page containing service descriptions and pricing
        :return:
        ***REMOVED***
        self.check_parameters(name=name, category=category, description=description)

        if self.can_create_service(uid=uid, organization_id=organization_id):
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
                key: Optional[ndb.Key] = services_instance.put(retries=self._max_retries, timeout=self._max_timeout)
                if not isinstance(key, ndb.Key):
                    message: str = "Database Error: there was an error creating service"
                    raise DataServiceError(status=error_codes.data_service_error_code, description=message)

                message: str = '''Successfully created plan service you may proceed to 
                create payment plans for this service'''
                return jsonify({'status': False, 'message': message}), status_codes.successfully_updated_code

            message: str = '''Remote Error: Unable to create plan service please try again later or inform admin'''
            return jsonify({'status': False, 'message': message}), error_codes.remote_data_error

            # TODO Investigate how we can update services especially on paypal
            # TODO the steps that follows after creating a
            # TODO service will be integrated into memberships

        message: str = '''You are not authorized to create services in this organization'''
        return jsonify({'status': False, 'message': message}), error_codes.access_forbidden_error_code

    @use_context
    @handle_view_errors
    def update_service(self, service_id: Optional[str], organization_id: Optional[str], uid: Optional[str],
                       name: Optional[str], description: Optional[str], category: Optional[str],
                       image_url: Optional[str], home_url: Optional[str]) -> tuple:
        ***REMOVED***
            **update_service**
                given service id update service details

        :param service_id:
        :param organization_id:
        :param uid:
        :param name:
        :param description:
        :param category:
        :param image_url:
        :param home_url:
        :return:
        ***REMOVED***
        self.check_parameters(name=name, category=category, description=description)

        if self.can_update_service(uid=uid, organization_id=organization_id, service_id=service_id):

            # TODO - first update service in paypal services

            service_instance: Optional[Services] = Services.query(Services.service_id == service_id).get()

            if isinstance(service_instance, Services):
                service_instance.name = name
                service_instance.description = description
                service_instance.category = category
                service_instance.image_url = image_url
                service_instance.home_url = home_url
                key: Optional[ndb.Key] = service_instance.put(retries=self._max_retries, timeout=self._max_timeout)
                if not isinstance(key, ndb.Key):
                    message: str = "Database Error: Unable to update service details"
                    raise DataServiceError(status=error_codes.data_service_error_code, description=message)

                # TODO - update cache instances
                message: str = "Successfully updated service or product"
                return jsonify({'status': True, 'payload': service_instance.to_dict(),
                                'message': message}), status_codes.status_ok_code

            message: str = "Data not Found: unable to update service as service was not found"
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

        message: str = "User Not Authorized: cannot update service"
        return jsonify({'status': False, 'message': message}), error_codes.access_forbidden_error_code

    @use_context
    @handle_view_errors
    def service_activation(self, service_id: Optional[str], organization_id: Optional[str], uid: Optional[str],
                           is_active: bool) -> tuple:
        ***REMOVED***
            **activate_service**
                given a service_id activate a service.
                an active service is viewable by users
        :param is_active:
        :param service_id:
        :param organization_id:
        :param uid:
        :return: tuple -> response, status_code
        ***REMOVED***
        if not isinstance(is_active, bool):
            message: str = "is_active: can only be a boolean"
            raise InputError(status=error_codes.input_error_code, description=message)

        if self.can_update_service(service_id=service_id, organization_id=organization_id, uid=uid):
            service_instance: Optional[Services] = Services.query(Services.service_id == service_id).get()

            if isinstance(service_instance, Services):
                service_instance.is_service_active = is_active
                key: Optional[ndb.Key] = service_instance.put(retries=self._max_retries, timeout=self._max_timeout)
                if not isinstance(key, ndb.Key):
                    message: str = "Database Error: unable to activate service"
                    raise DataServiceError(status=error_codes.data_service_error_code, description=message)
                # TODO - update cache
                message: str = "successfully activated service"
                return jsonify({'status': True, 'payload': service_instance.to_dict(),
                                'message': message}), status_codes.status_ok_code

            message: str = "Data not Found: unable to update service as service was not found"
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

        message: str = "User Not Authorized: cannot update service"
        return jsonify({'status': False, 'message': message}), error_codes.access_forbidden_error_code




