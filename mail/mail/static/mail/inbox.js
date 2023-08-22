document.addEventListener('DOMContentLoaded', function () {

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
    document.querySelector('#email').style.display = 'none';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3> <ul id="lista">
    </ul>`;
    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
            emails.forEach(email => {
                const nElement = document.createElement('li');
                if (email.archived === false) {
                    nElement.innerHTML = `<button class="btn btn-sm btn-outline-primary" onclick="switchArchive(${email.id}, true)">Archive</button><div class="liMail"><span class="info"><strong>${email.sender}</strong> <span>${email.subject}</span></span> <span class="timestamp">${email.timestamp}</span></div>`;
                    nElement.querySelector('.liMail').addEventListener('click', () => load_email(`${email.id}`));
                } else {
                    nElement.innerHTML = `<button class="btn btn-sm btn-outline-primary" onclick="switchArchive(${email.id}, false)">Unarchive</button><div class="liMail"><span class="info"><strong>${email.sender}</strong> <span>${email.subject}</span></span> <span class="timestamp">${email.timestamp}</span></div>`;
                    nElement.querySelector('.liMail').addEventListener('click', () => load_email(`${email.id}`));
                }
                if (email.read === true) {
                    nElement.querySelector('.liMail').classList.add('read');
                }
                const ElLista = document.querySelector("#lista");
                document.querySelector("#lista").append(nElement);
            });
        });

}

const sendEmail = (event) => {
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
const load_email = (id) => {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email').style.display = 'block';

    fetch(`/emails/${id}`)
        .then(response => response.json())
        .then(email => {
            document.querySelector('#email-from').innerHTML = email.sender;
            document.querySelector('#email-to').innerHTML = email.recipients;
            document.querySelector('#email-subject').innerHTML = email.subject;
            document.querySelector('#email-timestamp').innerHTML = email.timestamp;
            document.querySelector('#email-body').innerHTML = email.body;
            let jason = JSON.stringify(email);
            console.log(jason);
            document.querySelector('#reply').addEventListener('click', () => compose_reply(email));
        });
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    });


};

function switchArchive(id, bool) {
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: Boolean(bool)
        })
    });
    location.reload();
}

function compose_reply(email) {
    console.log(email);

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email').style.display = 'none';

    document.querySelector('#compose-recipients').value = `${email.sender}`;
    if(email.subject.substring(0,3) == "Re:") document.querySelector('#compose-subject').value = `${email.subject}`;
    else document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n ${email.body}`;

    /*await fetch(`/emails/${id}`)
        .then(response => response.json())
        .then(email => {
                            sender = email.sender;
                            subject = email.subject
                            body = email.body;
            });*/
    console.log(email);
    // Clear out composition fields
}