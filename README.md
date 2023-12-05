Note: this is not a blogsite, well technically it started out as a blogsite project, but deviated towards a credential management system, the password_locker being the cms.
# Credential Management System (CMS)
Welcome to the Credential Management System (CMS) project! This system is designed to provide a secure and efficient solution for managing credentials, utilizing advanced features such as RFID two-factor authentication, CRUD operations, and RSA7680 asymmetric encryption, all powered by the django web framework.

### Overview
The CMS is built using the Django web framework, incorporating HTML, Tailwind CSS, Bootstrap for styling, and JavaScript for enhancing webpage functionality.

### Key Features
RFID Two-Factor Authentication
Enhance security with RFID two-factor authentication, ensuring a robust access control mechanism for users.

### CRUD Operations
Users can perform CRUD operations to manage their credentials seamlessly. This includes creating, reading, updating, and deleting credentials based on their permissions.

### RSA7680 Asymmetric Encryption
Utilizing the RSA7680 asymmetric encryption algorithm provides a high level of security for credential storage and retrieval. This advanced encryption mechanism ensures that user credentials remain confidential, even in the face of evolving security threats.

Note: Avoiding RSA2048 
We've opted for RSA7680 instead of the commonly used RSA2048 due to concerns raised by MIT researchers in 2019, where RSA2048 was reportedly cracked by quantum computers. By using RSA7680, we aim to stay ahead of potential security risks.

Link: https://www.technologyreview.com/2019/05/30/65724/how-a-quantum-computer-could-break-2048-bit-rsa-encryption-in-8-hours/
