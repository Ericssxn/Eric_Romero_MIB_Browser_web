import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

async def snmpnext(version, rocommunity, agent, mib, oid):
    snmpEngine = SnmpEngine()

    iterator = next_cmd(
        snmpEngine,
        CommunityData(rocommunity, mpModel=version),
        await UdpTransportTarget.create((agent, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
        lexicographicMode=False
    )

    varBindsArray = []

    async for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            print(f"Error: {errorIndication}")
            break

        elif errorStatus:
            print(
                "{} at {}".format(
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1][0] or "?"
                )
            )
            break
        else:
            for varBind in varBinds:
                print(" = ".join([x.prettyPrint() for x in varBind]))
                varBindsArray.append(tuple(x.prettyPrint() for x in varBind))

            break

    snmpEngine.close_dispatcher()
    return varBindsArray
