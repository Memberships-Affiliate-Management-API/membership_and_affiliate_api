/**
 * subscribe page scripts: handles new user subscriptions for Memberships & Affiliates Management API Main APP
 **/


self.addEventListener('load', async e => {
    /** event listener to help load a submit event listener for new user subscriptions **/
    const subscribe_form = document.getElementById('subscribe')
    subscribe_form.addEventListener('submit', async e => {
        /** submit event listener for new user subscriptions form **/
        e.preventDefault();
        const names = document.getElementById('names').value
        const cell = document.getElementById('cell').value
        const email = document.getElementById('email').value
        const password = document.getElementById('password').value
        const repeat_password = document.getElementById('repeat-password').value
        const terms = document.getElementById('terms').checked
        /**
         *  check if names, cell, email, password, repeat_password
         * @type {*}
         */

        if ((terms === false) || (password === '') ||
            (password !== repeat_password)) {
            document.getElementById('message').innerHTML = 'please accept <code>terms</code> and insure ' +
                '<code>password</code> is not empty and <code>repeat password match</code>'
            return null
        }
        const response = await do_subscribe(names, cell, email, password)
        if (response.status === false) {
            document.getElementById('message').innerHTML = `${response.message}`
            return null
        }

    })
})


async function do_subscribe(names, cell, email, password){
    /** function used to actually subscribe and then login if success flask will redirect to dashboard and flash message
     *  otherwise it will return the error message
     */
    if ((email !== '') && (cell !== '') && (names !== '') && (password !== '')){
        console.log(`fields are being captured ${email} ${cell} ${names} ${password}`)
        //TODO- add authentication fields
        const request_par = {
            method: 'POST',
            headers: new Headers({'Content-Type': 'application/json'}),
            body: JSON.stringify({email,cell, names, password}),
            mode: 'cors',
            credentials: 'same-origin',
            cache: 'no-cache'
        }
        const url = '/api/v1/main/auth/subscribe'
        const request = new Request(url, request_par)
        const response = await fetch(request)
        return await response.json()
    }
    document.getElementById('message').innerHTML= 'please specify all <code>required fields</code>'
}