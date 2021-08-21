#### Recruits API Documentation

        **recruits**
            Allows Users and Clients to recruit other users and clients to
            their organizations.

        **PATH PARAMETERS**
            1. get -> retrieve a single recruit, expects organization_id and affiliate_id on recruit_data,
               user may supply the data as json body

            2. register -> used to register a single recruit, data as json must contain referrer_uid and
               organization_id, this allows multiple ways by which recruiters may recruit their affiliates

            3. delete -> soft delete a recruit by affiliate_id , organization_id is required

            4. activate -> mark recruit as active  : required parameters organization_id and affiliate_id

            5. de-activate -> de-activate recruit : required parameters organization_id and affiliate_id

            6. get-active -> returns active recruits : required parameters organization_id

            7. get-in-active -> get in-active recruits : required parameters organization_id

