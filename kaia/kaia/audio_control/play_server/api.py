from kaia.infra.marshalling_api import MarshallingEndpoint
import requests

class PlayApi:
    def __init__(self, address: str):
        MarshallingEndpoint.check_address(address)
        self.address = address

    def ping(self):
        requests.get(f'http://{self.address}')

    def play(self, content: bytes):
        requests.post(
            f'http://{self.address}/play',
            data=content,
            headers={'Content-Type': 'binary/octet-stream'}
        )


    def volume(self, volume: float):
        requests.post(
            f'http://{self.address}/volume',
            json=dict(volume=volume)
        )
