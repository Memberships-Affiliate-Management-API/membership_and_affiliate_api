/**
 * Forget Password & Recovery page scripts: for Memberships & Affiliates Management API
 */
self.addEventListener('load', async e => {
/** forget page event listener it helps to setup a submit event listener **/
    const form_forget = document.getElementById('forget');
    form_forget.addEventListener('submit', async e => {
        /** submit page event listener its purpose is to call the recover password function and then
         * print out a response to the user **/
        e.preventDefault()
        const email = document.getElementById('email').value
        // call submit recovery email
        const response = await send_recovery_email(email)
        /** whatever the response tell the user **/
        document.getElementById('message').innerHTML = `${response.message}`

    })
})


async function send_recovery_email(email){
/** recover email will send the email address to the backend and then retrieve a response, response is always positive*/
    /** if not Undefined or Null **/
    if (!!email){
        //TODO- authentication not required
        const request_par = {
                method : 'POST',
                headers: new Headers({'Content-Type': 'application/json'}),
                body : JSON.stringify({email}),
                mode: "cors",
                credentials: "same-origin",
                cache: "no-cache",
        }
        const url = '/api/v1/main/auth/send-recovery-email'
        const request = new Request(url, request_par);
        const response = await fetch(request)
        return await response.json()
    }
    /** email is undefined or Null **/
    document.getElementById('message').innerHTML = 'please enter the <code>email address</code> ' +
        'attached to your account for <code>password recovery</code>'
}