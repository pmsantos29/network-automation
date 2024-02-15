import asyncio
import telnetlib3

async def shell(reader, writer):
    rules = [
            (') >', 'enable'),
            (') #', 'show ip int brief'),
            (') #', 'exit')
            ]

    ruleiter = iter(rules)
    expect, send = next(ruleiter)
    while True:
        outp = await reader.read(1024)
        if not outp:
            break

        if expect in outp:
            writer.write(send)
            writer.write('\r\n')
            try:
                expect, send = next(ruleiter)
            except StopIteration:
                break

        # display all server output
        print(outp, flush=True)

    # EOF
    print()

async def main():
    reader, writer = await telnetlib3.open_connection('localhost', 5002, shell=shell)
    await writer.protocol.waiter_closed


if __name__ == '__main__':
    asyncio.run(main())
