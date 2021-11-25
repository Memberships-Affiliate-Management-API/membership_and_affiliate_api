from _swagger_api import ViewModel


class MembershipsView(ViewModel):
    """
        ** Class  MembershipsView **
            View model for Memberships
            
    """
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    method_decorators = []

    def __init__(self):
        pass
    
    @staticmethod
    def get(self,**paylod):
        """
        Get all memberships
        """
        pass
    


    @staticmethod
    def post(self, **payload):
        """
        Create a new membership
        """
        pass

    @staticmethod
    def put(self, **payload):
        """
        Update a membership
        """
        pass

    @staticmethod
    def delete(self, **payload):
        """
        Delete a membership
        """
        pass
