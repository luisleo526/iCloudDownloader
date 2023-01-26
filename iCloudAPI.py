import os
import sys
from pathlib import Path
from shutil import copyfileobj

from pyicloud import PyiCloudService


class API:

    def __init__(self, username, password):
        self.api = PyiCloudService(username, password)

        if self.api.requires_2fa:
            print("Two-factor authentication required.")
            code = input("Enter the code you received of one of your approved devices: ")
            result = self.api.validate_2fa_code(code)
            print("Code validation result: %s" % result)

            if not result:
                print("Failed to verify security code")
                sys.exit(1)

            if not self.api.is_trusted_session:
                print("Session is not trusted. Requesting trust...")
                result = self.api.trust_session()
                print("Session trust result %s" % result)

                if not result:
                    print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
        elif self.api.requires_2sa:
            import click
            print("Two-step authentication required. Your trusted devices are:")

            devices = self.api.trusted_devices
            for i, device in enumerate(devices):
                print(
                    "  %s: %s" % (i, device.get('deviceName',
                                                "SMS to %s" % device.get('phoneNumber')))
                )

            device = click.prompt('Which device would you like to use?', default=0)
            device = devices[device]
            if not self.api.send_verification_code(device):
                print("Failed to send verification code")
                sys.exit(1)

            code = click.prompt('Please enter validation code')
            if not self.api.validate_verification_code(device, code):
                print("Failed to verify verification code")
                sys.exit(1)

    def download(self, path, directory="."):
        file = self.api.drive
        for p in path.split('/'):
            file = file[p]
        if file.type == 'file':
            Path(directory).mkdir(parents=True, exist_ok=True)
            with file.open(stream=True) as response:
                with open(os.path.join(directory, file.name), 'wb') as file_out:
                    copyfileobj(response.raw, file_out)
        else:
            print("Check the file path, it's not a file!")
