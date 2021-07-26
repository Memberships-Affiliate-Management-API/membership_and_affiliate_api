/**
 * Forget page scripts: for Memberships & Affiliates Management API
 */

self.addEventListener('load', async e => {
/** forget page event listener it helps to setup a submit event listener **/
    console.log('forget page loaded')
    const form_forget = document.getElementById('forget');
    form_forget.addEventListener('submit', async e => {
        /** submit page event listener its purpose is to call the recover password function and then
         * print out a response to the user **/
        e.preventDefault()
        console.log('recover triggered')
        const email = document.getElementById('email').value
        console.log(`email : ${email}`)
        // call submit recovery email
        const response = await recover_email(email)
        if (response.status === true){
            document.getElementById('message').innerHTML = `${response.message}`
        }
    })
})


async function recover_email(email){
/** recover email will send the email address to the backend and then retrieve a response, response is always positive*/
    console.log(`Email Passed: ${email}`)
    if (email !== ''){
        const request_par = {
                method : 'POST',
                headers: new Headers({'Content-Type': 'application/json'}),
                body : JSON.stringify({email}),
                mode: "cors",
                credentials: "same-origin",
                cache: "no-cache",
        }
        const url = '/api/v1/main/auth/recover'
        const request = new Request(url, request_par);
        const response = await fetch(request)
        console.log(response)
        const response_object = await response.json()
        console.log(response_object)
        return response_object
    }
    document.getElementById('message').innerHTML = 'please enter the <code>email address</code> ' +
        'attached to your account for <code>password recovery</code>'
}