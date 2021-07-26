/***
 * contact page scripts: for Memberships & Affiliates Management API
 */

self.addEventListener('load', async e => {
    /** contact page event listener loaded, in order to insert the submit listener on contact form **/
    const contact_form = document.getElementById('contact')
    contact_form.addEventListener('submit', async e => {
        /** contact form event listener used to send contact information on success or failure notify
         * through message container
         **/
        e.preventDefault()
        const names = document.getElementById('names').value
        const email = document.getElementById('email').value
        const cell = document.getElementById('cell').value
        const topic = document.getElementById('topic').value
        const subject = document.getElementById('subject').value
        const body = document.getElementById('body').value
        const response = await do_send_contact(names, email, cell, topic, subject, body)
        document.getElementById('message').innerHTML =`${response.message}`
    })
})


async function do_send_contact(names, email, cell, topic, subject, body){
        if ((names !== '') && (email !== '') && (cell !== '') && (topic !== '') && (subject !== '') && (body !== '')){
        // TODO add authentication fields , if available
        const request_par = {
            method: 'POST',
            headers: new Headers({'Content-Type': 'application/json'}),
            body: JSON.stringify({names, email, cell, topic, subject, body}),
            mode: 'cors',
            credentials: 'same-origin',
            cache: 'no-cache'
        }
        const url = '/api/v1/main/contact'
        const request = new Request(url, request_par)
        const response = await fetch(request)
        return await response.json()
        }
        document.getElementById('message').innerHTML= 'please insure that all <code>required fields</code> are ' +
            'correctly filled in'
}