# EmailSpammer

A python script which sends an HTML email one-by-one to recepients

## Running the spammer

### Required files

1. `email_meta.json`
   * Contains the subject of the emails and the Gmail account stuff
2. `email.html`
   * The email you wish to spam in HTML form
3. `recipients.txt`
   * The list of recipients for the email

### Running the script

Run the script in the following style:

```bash
python3 ./EmailSpammer.py ./email_meta.json ./recipients.txt ./email.html
```

For more information, run the command `python3 ./EmailSpammer.py --help`.

---

Saku Rautio, 2020
