import asyncio
import time

from zepben.auth import create_authenticator

from zepben.evolve import connect, NetworkConsumerClient, NetworkService, connect_async


async def main():
    with open("C:/Users/marcu/ewb/ca.crt", "rb") as f:
        ca = f.read()
    with open("C:/Users/marcu/ewb/ca2.crt", "rb") as f:
        ca2 = f.read()
    authenticator = create_authenticator(conf_address="https://ewb.local:9000/ewb/auth", verify_certificate=False,
                                         auth_type_field="authType", audience_field="audience",
                                         issuer_domain_field="issuer")
    authenticator.token_request_data.update({
        'grant_type': 'password',
        'client_id': "8LCZNel8deS6Rcpt9Fv4ZgVMCzXI9uJ3",
        'username': "somerandomuser@bouckaert.com.au",
        'password': "Giraffe1354211",
        'scope': 'offline_access openid profile email0'
    })
    time.sleep(1)  # TODO: THE TOKENS BEGIN BEING VALID TOO LATE SO WE HAVE TO WAIT! or we invented time travel
    async with connect_async(host="ewb.local", rpc_port=50052,
                             secure=True,
                             client_id="8LCZNel8deS6Rcpt9Fv4ZgVMCzXI9uJ3",
                             username="somerandomuser@bouckaert.com.au",
                             password="Giraffe1354211",
                             conf_address="https://ewb.local:9000/ewb/auth",
                             ca=ca2) as channel:
        print("Connection Established")

        client = NetworkConsumerClient(channel)
        result = (await client.get_equipment_container(mrid="_WODEN_8_NB_STREETON")).throw_on_error().value
        ns: NetworkService = client.service
        print(result.objects["_WODEN_8_NB_STREETON"])


if __name__ == "__main__":
    asyncio.run(main())
