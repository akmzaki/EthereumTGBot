# (c) @AbirHasan2005

import logging
from aioify import aioify
from configs import Configs
from scanner import Etherscan
from pyrogram import Client, filters, types, enums

logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()],
    level=logging.INFO
)
bot = Client(
    name="pyrogram",
    in_memory=True,
    api_id=Configs.API_ID,
    api_hash=Configs.API_HASH,
    bot_token=Configs.BOT_TOKEN
)


@bot.on_message(filters.command("start"))
async def start_cmd(_, m: "types.Message"):
    return await m.reply_text("Hi, I'm Alive.", True)


@bot.on_message(filters=filters.command("set_wallet"))
async def set_wallet_cmd(_bot: Client, m: "types.Message"):
    if m.chat.id not in Configs.CHAT_IDS:
        return
    chat_member = await _bot.get_chat_member(chat_id=m.chat.id, user_id=m.from_user.id)
    if chat_member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await m.reply_text("You are not admin !!", True)
    if "set_wallet" in m.text.split(" ", 1)[-1]:
        return await m.reply_text("Send wallet Address after /set_wallet command !!", True)
    Configs.WALLET = m.text.split(" ", 1)[-1]
    await m.reply_text(f"**Set Wallet Address:** `{Configs.WALLET}`")


@bot.on_message(filters=filters.command("status"))
async def status_cmd(_, m: "types.Message"):
    # if (m.chat.id not in Configs.CHAT_IDS) or (m.chat.type != enums.ChatType.PRIVATE):
    #     return
    try:
        eth_balance, eth_value = await aioify(obj=Etherscan(wallet=Configs.WALLET).get_wallet_balance)()
    except Exception as err:
        return await m.reply_text(f"**Error:** {err}")
    await m.reply_animation(
        animation="giphy.gif.mp4",
        caption=Configs.STATUS_TEXT.format(eth_balance, eth_value),
        quote=True
    )


bot.run()
