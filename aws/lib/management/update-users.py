from botocore.exceptions import ClientError
import boto3
import csv
from datetime import datetime
from email.mime.text import MIMEText
from pprint import pformat, pprint
import secrets
import smtplib
import string

path_prefix = '/CITS5503/'
alphabet = string.ascii_letters + string.digits


def get_password(password_length):
    return ''.join(secrets.choice(alphabet) for i in range(password_length))



from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--debug',
                            action='store_true',
                            dest='debug',
                            default=False,
                            help='prints debug statements')

    def handle(self, *args, **options):
        """

        :param args:
        :param options:
        :return:
        """
        boto3.setup_default_session(profile_name='cits5503')
        iam_client = boto3.client('iam')
        iam_resource = boto3.resource('iam')
        cloud_computing_group = iam_resource.Group('CloudComputing')

        passwords = {}
        update_password = input('Overwrite all passwords Y/n?') == 'Y'


        print('Creating/updating accounts for all students in csv file...')

        with open('iam-users.csv') as fp:
            reader = csv.reader(fp)

            for row in reader:
                # last_name = row[0]
                # first_name = row[1]
                email = row[1]
                print(email)

                try:
                    response = iam_client.create_user(
                        Path=path_prefix,
                        UserName=email,
                    )
                    # pprint(response)
                except ClientError:
                    print('user already exists for {}'.format(email))

                try:
                    cloud_computing_group.add_user(UserName=email)
                except ClientError:
                    print('user already in cloud computing group {}'.format(email))

                temp_password = get_password(8)

                try:
                    response = iam_client.create_login_profile(
                        UserName=email,
                        Password=temp_password,
                        PasswordResetRequired=True,
                    )
                    passwords[email] = temp_password
                    pprint(response)
                except ClientError:

                    if update_password:
                        response = iam_client.update_login_profile(
                            UserName=email,
                            Password=temp_password,
                            PasswordResetRequired=True,
                        )
                        passwords[email] = temp_password
                        print('password reset for {}'.format(email))
                    else:
                        passwords[email] = ''
                        print('user already has a password set {}'.format(email))


                try:
                    iam_client.create_access_key(
                        UserName=email
                    )
                except:
                    pass

        print('done')

        # print('Removing accounts for students no longer in the unit...')
        #
        # response = iam_client.list_users(PathPrefix=path_prefix)
        #
        # for user in response['Users']:
        #     email = user['UserName']
        #     if email not in passwords:
        #         try:
        #             cloud_computing_group.remove_user(UserName=email)
        #         except ClientError:
        #             pass
        #         try:
        #             iam_client.delete_login_profile(UserName=email)
        #         except ClientError:
        #             pass
        #         try:
        #             iam_client.delete_user(UserName=email)
        #         except ClientError:
        #             pass
        #
        #         print('{} still enrolled? {} - deleted'.format(email, email in passwords))
        #     else:
        #         print('{} still enrolled? {}'.format(email, email in passwords))
        #
        # with open('temp-passwords-{}.txt'.format(str(datetime.now()).replace(':', '').replace('.', '').replace(' ', '').replace('-', '')), 'w') as fp:
        #     fp.write(pformat(passwords, indent=4))
        #
        #
        # # smtpserver = smtplib.SMTP(host='antivirus.uwa.edu.au')
        #
        # smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        # smtpserver.ehlo()
        # smtpserver.starttls()
        # smtpserver.ehlo()
        # response = smtpserver.login('john.pham@csp.uwa.edu.au', 'pueblo89')
        # print(response)
        #
        # for email, password in passwords.items():
        #
        #     text = 'The following are your user credentials for accessing AWS.\n\n' \
        #            'IAM user name: {email}\n' \
        #            'Temporary password: {password}\n\n' \
        #            'Please can you sign in as soon as possible and set a new password..\n' \
        #            'https://cits5503.signin.aws.amazon.com/console\n\n' \
        #            'If you have any issues contact help@csp.uwa.edu.au.'.format(
        #         email=email,
        #         password=password,
        #     )
        #
        #     msg = MIMEText(text)
        #     msg['Subject'] = 'CITS5503 AWS Credentials'
        #     msg['From'] = 'CITS5503@uwa.edu.au'
        #     msg['To'] = email
        #     # msg['To'] = 'mahp.jp@gmail.com'
        #
        #     smtpserver.send_message(msg)
        # #     print(msg)
        #

