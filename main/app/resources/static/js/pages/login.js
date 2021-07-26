/**
 * Login page scripts: for Memberships & Affiliates Management API
 */

self.addEventListener('load', async e => {
/** event listener to load an event listener for login submit event **/
    console.log('login page script loaded')
    const login_form = document.getElementById('login')
    login_form.addEventListener('submit', async e => {
        /** login submit event listener used to send login request only backend will handle page flow on success **/
        e.preventDefault();
        console.log('submit triggered on login page')
        const email = document.getElementById('email').value
        console.log(`Email Address ${email}`)
        const password = document.getElementById('password').value
        const response = await do_login(email, password)
        /** NOTE: flask app will automatically redirect user and display the login successfull message on success**/
        console.log(`response : ${response}`)
        if (response.status === false){
            /** if response is false then display message as the user isn't redirected login failed **/
            document.getElementById('message').innerHTML = `${response.message}`
        }
    })
})


async function do_login(email, password){
    console.log(`do_login called with ${'Email: '+ email + ' password: ' + password}`)
    if ((email !== '') && (password !== '')){
        const request_par = {
            method: 'POST',
            headers: new Headers({'Content-Type': 'application/json'}),
            body: JSON.stringify({email, password}),
            mode: 'cors',
            credentials: 'same-origin',
            cache: 'no-cache'
        }
        const url = '/api/v1/main/auth/login'
        const request = new Request(url, request_par)
        const response = await fetch(request)
        console.log(response)
        const response_object = await response.json()
        console.log(response_object)
        return response_object
    }
    document.getElementById('message').innerHTML='Please enter <code>email</code> and <code>password</code> ' +
        'combination for your account in order to login'
}