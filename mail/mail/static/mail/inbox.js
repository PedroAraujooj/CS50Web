document.addEventListener('DOMContentLoaded', function () {
    const sendEmail = async (event) => {
        event.preventDefault();
        let recipients = document.getElementById("compose-recipients").value;
        console.log(recipients);
        let subject = document.getElementById("compose-subject").value;
        console.log(subject);
        let body = document.getElementById("compose-body").value;
        console.log(body);
        fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
                recipients: recipients,
                subject: subject,
                body: body
            })
        }).then(response => response.json()).then(result => {
            console.log(result);
        });
        load_mailbox('sent');
    };
    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#sendEmail').addEventListener('click', (event) => sendEmail(event));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3> <ul id="lista">
    </ul>`;
    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
            emails.forEach(email => {
                console.log(email);
                console.log(mailbox);
                const nElement = document.createElement('li');
                console.log(nElement);
                console.log(email);
                nElement.innerHTML = `<strong>${email.sender}</strong> <p>${email.body}</p> <p id="timestamp">${email.timestamp}</p>`;
                const ElLista = document.querySelector("#lista");
                console.log(ElLista);
                document.querySelector("#lista").append(nElement);
                console.log(document.getElementById("lista"));
            });
        });

}

