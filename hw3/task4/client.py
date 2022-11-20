import asyncio
import websockets
import hashlib
import os

EMAIL = "your.email@epfl.ch"
PASSWORD = "correct horse battery staple"
N = int("EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3", base=16)
g = 2

def generate_randomint32():
    n_bits = 32
    result = int.from_bytes(os.urandom(n_bits), 'big')
    return result


async def pake():
    async with websockets.connect("ws://localhost:5000") as websocket:
        await websocket.send(EMAIL.encode())
        salt_hex = await websocket.recv()

        a = generate_randomint32() 
        A = pow(g, a, N)
        A_hex = format(A, "x").encode()
        await websocket.send(A_hex)
        B_hex = await websocket.recv()
        B = int(B_hex, base=16)

        h = hashlib.sha256()
        h.update(A_hex)
        h.update(B_hex)
        u_hex = h.hexdigest()
        u = int(u_hex, base=16)

        email_with_pass = f"{EMAIL}:{PASSWORD}"
        inner = hashlib.sha256()
        inner.update(email_with_pass.encode())
        hashed_email = inner.hexdigest()

        outer = hashlib.sha256()
        outer.update(salt_hex)
        outer.update(hashed_email.encode())

        x = int(outer.hexdigest(), 16)
        S = pow(B - pow(g, x, N), (a + u * x), N)
        
        h = hashlib.sha256()
        h.update(A_hex)
        h.update(B_hex)
        h.update(format(S, 'x').encode())
        await websocket.send(h.hexdigest().encode())

        resp = await websocket.recv()
        print("Response: {}".format(resp))


if __name__ == "__main__":
    asyncio.run(pake())