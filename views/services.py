***REMOVED***
    Services View , will handle service Creation
    on the database and also on paypal
***REMOVED***
from flask import jsonify, current_app
# noinspection PyProtectedMember
from _sdk._paypal.paypal import PayPalRecurring
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

        if self.can_create_service(uid=uid, organization_id=organization_id) is True:
            if name is None or name == "":
                message: str = "Service Name cannot be Null"
                return jsonify({'status': False, 'message': message}), 500
            if description is None or description == "":
                message: str = "Service Description cannot be Null"
                return jsonify({'status': False, 'message': message}), 500
            if category is None or category == "":
                message: str = "Service Category cannot be Null"
                return jsonify({'status': False, 'message': message}), 500

            name = str(name).strip().lower()
            services_instance: Services = Services.query(Services.name == name,
                                                         Services.organization_id == organization_id).get()

            if isinstance(services_instance, Services):
                message: str = 'a service with that name already exist in your organization please use a different name'
                return jsonify({'status': False, 'message': message}), 500
            # TODO create service in paypal obtain service_id
            paypal_services_instance: PayPalRecurring = PayPalRecurring(app=current_app, custom_id=organization_id)
            paypal_services_instance.set_service_details(name=name, description=description, category=category,
                                                         image_url=image_url, home_url=home_url)

            # TODO -Alternatively Use webhooks to capture the results of service creation also
            service_response = paypal_services_instance.create_service()
            if service_response.status_code == 201:
                service_id = service_response.result.id
                services_instance: Services = Services(organization_id=organization_id, created_by_uid=uid,
                                                       service_id=service_id, name=name, description=description,
                                                       category=category, image_url=image_url, home_url=home_url)
                key = services_instance.put(retries=self._max_retries, timeout=self._max_timeout)

                message: str = '''Successfully created plan service you may proceed to 
                create payment plans for this service'''
                return jsonify({'status': False, 'message': message}), 200

            message: str = '''Unable to create plan service please try again later or inform admin'''
            return jsonify({'status': False, 'message': message}), 500

        message: str = '''You cannot create service plans for this organization 
        please inform your organization admin for assistance'''
        return jsonify({'status': False, 'message': message}), 500

        # TODO Investigate how we can update services especially on paypal
        # TODO the steps that follows after creating a
        #   service will be integrated into memberships
