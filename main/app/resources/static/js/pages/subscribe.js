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

        if ((terms === true) && (names !== '') && (cell !== '') && (email !== '') && (password !== '') &&
            (password === repeat_password)) {
            const response = await do_subscribe(names, cell, email, password)
            if (response.status === false) {
                console.log(`there was an error subscribing : ${response.message}`)
                document.getElementById('message').innerHTML = `${response.message}`
            }
        }
        document.getElementById('message').innerHTML= 'please specify all <code>required fields</code> ' +
            '<em>accept terms</em> and insure that <em>passwords match</em>'
    })
})


async function do_subscribe(names, cell, email, password){
    /** function used to actually subscribe and then login if success flask will redirect to dashboard and flash message
     *  otherwise it will return the error message
     */

}